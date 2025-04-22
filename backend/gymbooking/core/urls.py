from django.urls import path
from .views import (
    login_view, logout_view, GymListCreateView, GymDetailView, book_timestamp, register_view, GymOwnerAuthView, GymOwnerLoginView
)

urlpatterns = [
    path('login/', login_view),
    path('logout/', logout_view),
    path('login-gymowner/', GymOwnerLoginView.as_view()),
    path('gymowner-auth/', GymOwnerAuthView.as_view()),
    path('gyms/', GymListCreateView.as_view()),
    path('gyms/create/', GymListCreateView.as_view()),
    path('gyms/<int:pk>/', GymDetailView.as_view()),
    path('timestamps/<int:pk>/book/', book_timestamp),
]
