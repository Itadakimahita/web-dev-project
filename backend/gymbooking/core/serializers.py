from rest_framework import serializers
from .models import User, Gym, GymOwner, Timestamp
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone_number']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            phone_number=validated_data.get('phone_number')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class GymOwnerLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        if not hasattr(user, 'gym_owner'):
            raise serializers.ValidationError("User is not registered as a GymOwner")

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username
        }
    
class GymOwnerAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    license_number = serializers.CharField(required=False)

    def validate(self, data):
        username = data['username']
        password = data['password']
        license_number = data.get('license_number')

        user, created = User.objects.get_or_create(username=username)
        if created:
            user.set_password(password)
            user.save()
        else:
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials")

        if not hasattr(user, 'gym_owner'):
            if not license_number:
                raise serializers.ValidationError("GymOwner must provide license_number on first registration.")
            GymOwner.objects.create(user=user, license_number=license_number)

        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'username': user.username
        }


class BookingSerializer(serializers.Serializer):
    timestamp_id = serializers.IntegerField()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number']

class GymSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gym
        fields = '__all__'
        read_only_fields = ['created_by']

class TimestampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timestamp
        fields = '__all__'


