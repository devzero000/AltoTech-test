from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    @property
    def full_name(self) -> str:
        return f'{self.first_name} {self.last_name}'.strip()
