from rest_framework import serializers
from rest_framework.fields import IntegerField

from .models import EquipClub, UserRent


class EquipClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipClub
        fields = '__all__'


class EquipClubUpdateSerializer(serializers.Serializer):
    hour_rent = IntegerField(min_value=1)


class UserRentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRent
        fields = '__all__'


class UserRentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRent
        fields = ('discount', 'last_hour_rent', 'hour_sum',)
