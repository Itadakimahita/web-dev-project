from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, LogoutView, gym_list, gym_create, GymDetailView, TimestampBookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('gyms/', gym_list, name='gym_list'),
    path('gyms/create/', gym_create, name='gym_create'),
    path('gyms/<int:pk>/', GymDetailView.as_view(), name='gym_detail'),
    path('timestamps/<int:pk>/book/', TimestampBookView.as_view(), name='timestamp_book'),
]
