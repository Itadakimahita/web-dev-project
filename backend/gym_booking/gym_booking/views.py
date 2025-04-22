from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Gym, Timestamp
from .serializers import GymSerializer, TimestampSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gym_list(request):
    gyms = Gym.objects.active_gyms()
    serializer = GymSerializer(gyms, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def gym_create(request):
    serializer = GymSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user.gym_owner.first())
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GymDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            gym = Gym.objects.get(pk=pk)
            serializer = GymSerializer(gym)
            return Response(serializer.data)
        except Gym.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            gym = Gym.objects.get(pk=pk, created_by=request.user.gym_owner.first())
            serializer = GymSerializer(gym, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Gym.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            gym = Gym.objects.get(pk=pk, created_by=request.user.gym_owner.first())
            gym.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Gym.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class TimestampBookView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            timestamp = Timestamp.objects.get(pk=pk)
            if not timestamp.can_book():
                return Response({"error": "Timestamp is fully booked"}, status=status.HTTP_400_BAD_REQUEST)
            timestamp.current_bookings += 1
            timestamp.user = request.user
            timestamp.save()
            serializer = TimestampSerializer(timestamp)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Timestamp.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class CustomTokenObtainPairView(TokenObtainPairView):
    pass

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        return Response({"message": "Successfully logged out"}, status=200)