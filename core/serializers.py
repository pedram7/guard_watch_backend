from django.contrib.auth import authenticate

from rest_framework import serializers
from .models import *


class GuardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guard
        fields = ['name', 'staff_id', 'date_joined']


class BandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wristband
        fields = ['band_id']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="شناسه کاربری")
    password = serializers.CharField(label="رمز عبور", style={'input_type': 'password'}
                                     , write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])

        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User is disabled.')

        return {'user': user}


class LogInstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogInstance
        fields = ['lat', 'lang', 'heartbeat', 'emergency_alert', 'time']

    def validate(self, attrs):
        print("lksd")
        return attrs

    def to_internal_value(self, data):
        return data


class BulkLogSerializer(serializers.Serializer):
    band_id = serializers.CharField(required=True)
    data = LogInstanceSerializer(many=True)

    def create(self, validated_data):
        data = validated_data['data']
        objs = []
        for item in data:
            instance = LogInstance(**item)
            instance.wristband = Wristband.objects.get(band_id=validated_data['band_id'])
            objs.append(instance)

        LogInstance.objects.bulk_create(objs, ignore_conflicts=True)
