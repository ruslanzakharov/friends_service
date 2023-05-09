import enum


class FriendshipStatus(enum.Enum):
    """
    Класс, содержащий возможные статусы дружбы с пользователем.
    """

    INCOMING = 'incoming'
    OUTCOMING = 'outcoming'
    FRIENDS = 'friends'


class FriendshipAction(enum.Enum):
    """
    Класс, содержащий возможные действия пользователя с заявкой в друзья.
    """

    ACCEPT = 'accept'
    REJECT = 'reject'
