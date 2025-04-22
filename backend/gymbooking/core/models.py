from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class GymOwner(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gym_owner')
    license_number = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

class GymManager(models.Manager):
    def active_gyms(self):
        return self.filter(is_active=True)

class Gym(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(GymOwner, on_delete=models.CASCADE, related_name='gyms')
    objects = GymManager()

    def __str__(self):
        return self.name

class Timestamp(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE, related_name='timestamps')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    max_capacity = models.IntegerField(default=30)
    current_bookings = models.IntegerField(default=0)

    def can_book(self):
        return self.current_bookings < self.max_capacity

    def __str__(self):
        return f"{self.gym.name} - {self.start_time}"