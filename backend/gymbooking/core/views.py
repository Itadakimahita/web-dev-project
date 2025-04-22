from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Gym, Timestamp, User, GymOwner
from .serializers import (
    LoginSerializer, GymSerializer, TimestampSerializer, BookingSerializer, RegisterSerializer, GymOwnerAuthSerializer, GymOwnerLoginSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        user = User.objects.get(username=serializer.validated_data['username'])
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=404)

    if user.check_password(serializer.validated_data['password']):
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid password'}, status=401)
    
class GymOwnerAuthView(APIView):
    def post(self, request):
        serializer = GymOwnerAuthSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)
    
class GymOwnerLoginView(APIView):
    def post(self, request):
        serializer = GymOwnerLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=200)
        return Response(serializer.errors, status=400)

    
@api_view(['POST'])
def register_view(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({'message': 'User created successfully'}, status=201)
    return Response(serializer.errors, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    request.auth.delete()
    return Response({'detail': 'Logged out successfully'}, status=204)

class GymListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gyms = Gym.objects.all()
        serializer = GymSerializer(gyms, many=True)
        return Response(serializer.data)

    def post(self, request):
        gym_owner = GymOwner.objects.filter(user=request.user).first()
        if gym_owner is None:
            return Response({'error': 'Only GymOwners can add gyms.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = GymSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=gym_owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GymDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Gym.objects.get(pk=pk)
        except Gym.DoesNotExist:
            return Response({'error': 'Gym not found'}, status=404)

    def get(self, request, pk):
        gym = self.get_object(pk)
        if not gym:
            return Response({'error': 'Gym not found'}, status=404)
        serializer = GymSerializer(gym)
        return Response(serializer.data)

    def put(self, request, pk):
        gym = self.get_object(pk)
        if not gym:
            return Response({'error': 'Gym not found'}, status=404)
        serializer = GymSerializer(gym, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        gym = self.get_object(pk)
        if not gym:
            return Response({'error': 'Gym not found'}, status=404)
        gym.delete()
        return Response(status=204)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_timestamp(request, pk):
    try:
        timestamp = Timestamp.objects.get(pk=pk)
        if timestamp.can_book():
            timestamp.current_bookings += 1
            timestamp.save()
            timestamp.user.add(request.user)
            return Response({'success': 'Booked!'})
        return Response({'error': 'Full capacity'}, status=400)
    except Timestamp.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)
