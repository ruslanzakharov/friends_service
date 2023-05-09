from django.urls import path
from friends import views


urlpatterns = [
    path('user/', views.UserView.as_view()),
]
