from uuid import UUID

from friends.models import CustomUser, Friendship
from friends.enums import FriendshipStatus


class UserStorage:
    @staticmethod
    def get_user_by_id(user_id: UUID) -> CustomUser | None:
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return None


class FriendshipStorage:
    @staticmethod
    def get_friendship(user_id: UUID, friend_id: UUID) -> Friendship | None:
        try:
            return Friendship.objects.get(
                user_id=user_id, friend_id=friend_id
            )
        except Friendship.DoesNotExist:
            return None

    @staticmethod
    def create_friendship(
            user_id: UUID, friend_id: UUID, status: FriendshipStatus
    ) -> Friendship | None:
        friendship = Friendship(
            user_id=user_id, friend_id=friend_id, status=status.value
        )
        friendship_reversed = Friendship(
            user_id=friend_id, friend_id=user_id,
            status=status.reversed_status().value
        )

        Friendship.objects.bulk_create([friendship, friendship_reversed])

        return friendship

    @classmethod
    def change_status_to_friends(cls, friendship: Friendship) -> Friendship:
        friendship.status = FriendshipStatus.FRIENDS.value

        friendship_reversed = cls.get_friendship(
            friendship.friend_id, friendship.user_id
        )
        friendship_reversed.status = FriendshipStatus.FRIENDS.value

        Friendship.objects.bulk_update(
            [friendship, friendship_reversed], ['status']
        )

        return friendship

    @staticmethod
    def delete_friendship(friendship: Friendship) -> None:
        friendship_reversed = Friendship.objects.get(
            user_id=friendship.friend_id, friend_id=friendship.user_id
        )
        friendship.delete()
        friendship_reversed.delete()
