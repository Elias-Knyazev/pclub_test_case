from datetime import datetime, timezone, timedelta

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import EquipClub, UserRent
from .permissions import IsAdminOrReadOnly
from .serializers import EquipClubSerializer, UserRentListSerializer, UserRentUpdateSerializer, \
    EquipClubUpdateSerializer


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
        current_datetime = datetime.now(timezone(timedelta(hours=3)))

        for equip_club in EquipClub.objects.all():
            if equip_club.time_rent_end and (equip_club.time_rent_end < current_datetime):
                equip_club.is_busy = False
                equip_club.time_rent_start=None
                equip_club.time_rent_end=None
                equip_club.save()

        return Response(EquipClub.objects.filter(is_busy=False).values())

    permission_classes = (IsAuthenticated,)


class RentEquipAPIView(APIView):
    def patch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "pk was not provided"})

        try:
            instance = EquipClub.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({"error": "Object does not exists"})

        serializer = EquipClubUpdateSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        hour_rent = serializer.validated_data['hour_rent']
        print(request.data)
        print(serializer.validated_data)
        print(hour_rent)
        time_start = datetime.now(timezone.utc)
        time_delta = timedelta(hours=hour_rent)
        time_end = time_start + time_delta
        #time_end = time_end.strftime('%Y-%m-%d %H:%M')

        eq_data = {
            #'type': new_data.get('type'),
            #'eq_number': new_data.get('eq_number'),
            'hour_rent': hour_rent,
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
        else:
            discount = 1.0
        hour_sum += request.data.get("last_hour_rent")

        user_rent_data = {
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
