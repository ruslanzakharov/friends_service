from rest_framework import serializers
from friends.models import CustomUser, Friendship


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class FriendshipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Friendship
        fields = ['user_id', 'friend_id', 'status']
