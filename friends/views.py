from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from friends.serializers import UserSerializer
from friends.models import CustomUser
from friends.storage import UserStorage, FriendshipStorage
from friends.enums import FriendshipStatus


class UserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class FriendshipView(APIView):
    def post(self, request, user_id, friend_id):
        friendship = FriendshipStorage.get_friendship(user_id, friend_id)

        if friendship is None:
            friendship = FriendshipStorage.create_friendship(
                user_id, friend_id, FriendshipStatus.OUTCOMING
            )
        elif friendship.status == FriendshipStatus.INCOMING.value:
            friendship = FriendshipStorage.change_status_to_friends(
                friendship=friendship
            )
        elif friendship.status == FriendshipStatus.OUTCOMING.value:
            return Response(
                {'message': 'The user has already sent a friend request'},
                status=status.HTTP_409_CONFLICT
            )
        elif friendship.status == FriendshipStatus.FRIENDS.value:
            return Response(
                {'message': 'Users are already friends'},
                status=status.HTTP_409_CONFLICT
            )

        return Response(
            {
                'user_id': user_id,
                'friend_id': friend_id,
                'status': friendship.status
            },
            status=status.HTTP_200_OK
        )
