from datetime import datetime, timezone, timedelta
import time
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EquipClub, UserRent
from .permissions import IsAdminOrReadOnly
from .serializers import EquipClubSerializer, UserRentListSerializer, UserRentUpdateSerializer


class ECListAPIView(generics.ListCreateAPIView):
    queryset = EquipClub.objects.all()
    serializer_class = EquipClubSerializer
    permission_classes = (IsAdminOrReadOnly,)


class ECDeleteAPIView(generics.DestroyAPIView):
    queryset = EquipClub.objects.all()
    serializer_class = EquipClubSerializer
    permission_classes = (IsAdminOrReadOnly,)



class EquipClubNotBusyAPIView(APIView):
    def get(self, request):
        current_datetime = datetime.now(timezone.utc)
        for i in EquipClub.objects.all():
            if  i.time_rent_end != '0':
                time_rent_end = datetime.strptime(str(i.time_rent_end), '%Y-%m-%d %H:%M')
                if time_rent_end.timestamp() < current_datetime.timestamp():
                    EquipClub.objects.filter(id=i.id).update(is_busy=False, time_rent_start='0', time_rent_end='0')

        return Response(EquipClub.objects.filter(is_busy=False).values())

    permission_classes = (IsAuthenticated,)


class RentEquipAPIView(APIView):
    def put(self, request, *args, **kwargs):
        pk=kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = EquipClub.objects.get(pk=pk)

        except:
            return Response({"error": "Object does not exists"})

        new_data = request.data.copy()

        time_start = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M')
        time_delta = request.data.get('hour_rent')
        time_delta = timedelta(hours=time_delta)
        time_end = datetime.now(timezone.utc) + time_delta
        time_end = time_end.strftime('%Y-%m-%d %H:%M')

        eq_data = {
            'type': new_data.get('type'),
            'eq_number': new_data.get('eq_number'),
            'hour_rent': new_data.get('hour_rent'),
            'time_rent_start': time_start,
            'time_rent_end': time_end,
            'is_busy': True,
            }

        serializer = EquipClubSerializer(data=eq_data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"equip_rent": serializer.data})

    permission_classes = (IsAuthenticatedOrReadOnly,)


class UserRentListCreateAPIView(generics.ListCreateAPIView):
    queryset = UserRent.objects.all()
    serializer_class = UserRentListSerializer
    permission_classes = (IsAdminUser,)


class UserRentUpdateAPIView(generics.UpdateAPIView):
    def put(self, request, *args, **kwargs):
        user_id = request.data.get("user", None)

        if not user_id:
            return Response({"error": "Method PUT not allowed"})

        try:
            instance = UserRent.objects.get(user_id=user_id)

        except:
            return Response({"error": "Object does not exists"})

        hour_sum = UserRent.objects.get(user_id=user_id).hour_sum
        if hour_sum >= 100:
            discount = 0.9
        hour_sum += request.data.get("last_hour_rent")

        user_rent_data={
            'user_id': request.data.get('user_id'),
            'last_hour_rent': request.data.get('last_hour_rent'),
            'hour_sum': hour_sum,
            'discount': discount,
            }
        serializer = UserRentUpdateSerializer(data=user_rent_data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"user_rent": serializer.data})

    permission_classes = (IsAuthenticated,)






















