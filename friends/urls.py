from django.urls import path
from friends import views


urlpatterns = [
    path('user', views.UserView.as_view()),
    path(
        'user/<uuid:user_id>/friend/<uuid:friend_id>',
        views.FriendshipView.as_view()
    ),
]
