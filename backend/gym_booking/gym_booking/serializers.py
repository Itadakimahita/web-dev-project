from rest_framework import serializers
from .models import Gym, Timestamp, User, GymOwner

class GymSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=255)
    is_active = serializers.BooleanField(default=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        return Gym.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.address = validated_data.get('address', instance.address)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.save()
        return instance

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=150)
    phone_number = serializers.CharField(max_length=15, allow_blank=True, allow_null=True)

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance

class TimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timestamp
        fields = ['id', 'gym', 'user', 'start_time', 'end_time', 'max_capacity', 'current_bookings']
        read_only_fields = ['user', 'current_bookings']

class GymOwnerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GymOwner
        fields = ['id', 'user', 'license_number', 'created_at']