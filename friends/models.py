from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from friends import enums


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Friendship(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_friends')
    # related_name="+" отключает возможность получить пользователей по другу
    # Так как семантически это некорректно
    friend_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='+')
    status = models.CharField(
        max_length=30,
        choices=[(tag.name, tag.value) for tag in enums.FriendshipStatus]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'friend_id'], name='unique_friendship')
        ]

    def __str__(self):
        return f'{self.user_id} и {self.friend_id} имеют статус {self.status}'
