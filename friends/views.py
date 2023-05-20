from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from uuid import UUID

from friends.serializers import UserSerializer, FriendshipSerializer
from friends.models import CustomUser
from friends.storage import FriendshipStorage
from friends.enums import FriendshipStatus, FriendshipAction
from friends.utils.friendship import get_none_friendship


class UserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class FriendshipView(APIView):
    def post(
            self, request: Request, user_id: UUID, friend_id: UUID
    ) -> Response:
        try:
            user = CustomUser.objects.get(id=user_id)
            friend = CustomUser.objects.get(id=friend_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'message': 'At least one of the users does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

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
            FriendshipSerializer(friendship).data,
            status=status.HTTP_200_OK
        )

    def put(
            self, request: Request, user_id: UUID, friend_id: UUID
    ) -> Response:
        try:
            user = CustomUser.objects.get(id=user_id)
            friend = CustomUser.objects.get(id=friend_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'message': 'At least one of the users does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            action = FriendshipAction(request.query_params.get('action'))
        except ValueError:
            return Response(
                {'message': 'Invalid action type specified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        friendship = FriendshipStorage.get_friendship(user_id, friend_id)

        if friendship is None or friendship.status == FriendshipStatus.OUTCOMING.value:
            return Response(
                {'message': 'Friend request not received'},
                status=status.HTTP_409_CONFLICT
            )
        elif friendship.status == FriendshipStatus.INCOMING.value:
            if action == FriendshipAction.ACCEPT:
                FriendshipStorage.change_status_to_friends(friendship=friendship)
                return Response(
                    FriendshipSerializer(friendship).data,
                    status=status.HTTP_200_OK
                )
            elif action == FriendshipAction.REJECT:
                FriendshipStorage.delete_friendship(friendship)
                return Response(
                    {'message': 'Friend request rejected'}
                )
        elif friendship.status == FriendshipStatus.FRIENDS.value:
            return Response(
                {'message': 'Users are already friends'},
                status=status.HTTP_409_CONFLICT
            )

    def delete(
            self, request: Request, user_id: UUID, friend_id: UUID
    ) -> Response:
        try:
            user = CustomUser.objects.get(id=user_id)
            friend = CustomUser.objects.get(id=friend_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'message': 'At least one of the users does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        friendship = FriendshipStorage.get_friendship(user_id, friend_id)

        if friendship is None:
            return Response(
                {'message': 'Users are not friends'},
                status=status.HTTP_409_CONFLICT
            )
        if friendship.status == FriendshipStatus.FRIENDS.value:
            FriendshipStorage.delete_friendship(friendship)
            return Response(
                {'message': 'User removed from friends'},
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'message': 'Users are not friends'},
            status=status.HTTP_409_CONFLICT
        )

    def get(
            self, request: Request, user_id: UUID, friend_id: UUID
    ) -> Response:
        try:
            user = CustomUser.objects.get(id=user_id)
            friend = CustomUser.objects.get(id=friend_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'message': 'At least one of the users does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        friendship = FriendshipStorage.get_friendship(user_id, friend_id)

        if friendship is None:
            none_friendship = get_none_friendship(user_id, friend_id)
            return Response(
                    FriendshipSerializer(none_friendship).data,
                    status=status.HTTP_200_OK
            )
        return Response(
                FriendshipSerializer(friendship).data,
                status=status.HTTP_200_OK
        )


class FriendshipsView(APIView):
    def get(self, request: Request, user_id: UUID) -> Response:
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'message': 'User does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            f_status = FriendshipStatus(request.query_params.get('type'))
        except ValueError:
            return Response(
                {'message': 'Incorrect friendship status specified'},
                status=status.HTTP_400_BAD_REQUEST
            )
        friendships = FriendshipStorage.get_friendships_by_status(
            user, f_status
        )

        return Response(
            FriendshipSerializer(friendships, many=True),
            status=status.HTTP_200_OK
        )
