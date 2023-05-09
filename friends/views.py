from rest_framework import generics

from friends.serializers import UserSerializer
from friends.models import CustomUser


class UserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
