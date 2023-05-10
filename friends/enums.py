import enum


class FriendshipStatus(enum.Enum):
    """
    Класс, содержащий возможные статусы дружбы с пользователем.
    """

    INCOMING = 'incoming'
    OUTCOMING = 'outcoming'
    FRIENDS = 'friends'
    NONE = 'none'

    def reversed_status(self):
        if self.value == self.INCOMING.value:
            return self.OUTCOMING
        elif self.value == self.OUTCOMING.value:
            return self.INCOMING
        elif self.value == self.FRIENDS.value:
            return self.FRIENDS
        elif self.value == self.NONE.value:
            return self.NONE


class FriendshipAction(enum.Enum):
    """
    Класс, содержащий возможные действия пользователя с заявкой в друзья.
    """

    ACCEPT = 'accept'
    REJECT = 'reject'
