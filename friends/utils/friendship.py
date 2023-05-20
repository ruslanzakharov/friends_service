from uuid import UUID

from friends.models import Friendship
from friends.enums import FriendshipStatus


def get_none_friendship(user_id: UUID, friend_id: UUID) -> Friendship:
    return Friendship(
        user_id=user_id,
        friend_id=friend_id,
        friendship=FriendshipStatus.NONE.value
    )
