from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email_address, username, password=None, **extra_fields):
        if not email_address:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email_address = self.normalize_email(email_address)
        user = self.model(email_address=email_address, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email_address, username, password, **extra_fields)