from datetime import datetime

from dateutil.relativedelta import relativedelta
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Field
from django.db.models import Model
from django.db.models.fields.related import ForeignObject
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django_prometheus.models import ExportModelOperationsMixin
from django_rest_passwordreset.signals import reset_password_token_created
from phonenumber_field.modelfields import PhoneNumberField
from Project.storage import image_file_upload
from rest_framework.views import View
from Users.choices import GenderChoices
from Users.choices import PreferredLanguageChoices


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        **extra_fields: dict,
    ) -> Model:
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given email must be set")
        email: str = self.normalize_email(email)
        user: User = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        **extra_fields: dict,
    ) -> Model:
        """
        Create and save a SuperUser with the given email and password.
        """
        user: User = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_verified = True
        user.is_premium = True
        user.save(using=self._db)
        return user


class User(
    ExportModelOperationsMixin("dataset"), AbstractBaseUser, PermissionsMixin
):
    username: None = None
    is_superuser: None = None
    last_login: None = None

    email: Field = models.EmailField(
        "Email address",
        unique=True,
        error_messages={"unique": "This email already exists."},
    )
    first_name: Field = models.CharField(
        "First name", null=False, max_length=50
    )
    last_name: Field = models.CharField("Last name", null=False, max_length=50)
    phone_number: PhoneNumberField = PhoneNumberField(
        "Phone number",
        null=True,
        blank=True,
        max_length=22,
        unique=True,
        error_messages={"unique": "This number already exists."},
    )
    is_verified: Field = models.BooleanField("Verified", default=False)
    is_premium: Field = models.BooleanField("Premium", default=False)
    is_admin: Field = models.BooleanField("Admin", default=False)
    created_at: Field = models.DateTimeField(
        "Creation date", auto_now_add=True
    )
    updated_at: Field = models.DateTimeField("Update date", auto_now=True)

    USERNAME_FIELD: str = "email"
    REQUIRED_FIELDS: list = ["first_name", "last_name"]

    objects: BaseUserManager = CustomUserManager()

    def __str__(self) -> str:
        return self.email

    def save(self, *args: tuple, **kwargs: dict) -> None:
        super().save(*args, **kwargs)
        has_profile: bool = Profile.objects.filter(user=self).exists()
        if not has_profile and self.is_verified:
            self.create_profile()

    def create_profile(self) -> None:
        Profile.objects.create(user=self)

    def has_perm(self, permission: str, object: Model = None) -> bool:
        return self.is_admin

    def has_permission(self, object: Model = None) -> bool:
        if isinstance(object, User):
            return object.id == self.id
        else:
            return object.user.id == self.id

    def has_module_perms(self, app_label: str) -> bool:
        return self.is_admin

    def verify(self) -> None:
        self.is_verified = True
        self.save()

    @property
    def name(self) -> str:
        return self.first_name + " " + self.last_name

    @property
    def is_staff(self) -> bool:
        return self.is_admin


class Profile(models.Model):
    user: ForeignObject = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    nickname: Field = models.CharField(
        "Nick",
        unique=True,
        error_messages={"unique": "This nickname already exists."},
        null=True,
        max_length=50,
    )
    bio: Field = models.TextField("Bio", null=True)
    image: Field = models.ImageField(
        "Profile image",
        upload_to=image_file_upload,
        null=True,
    )
    gender: Field = models.CharField(
        "Gender",
        max_length=1,
        choices=GenderChoices.choices,
        default=GenderChoices.NOT_SAID,
        null=True,
    )
    preferred_language: Field = models.CharField(
        "Preferred language",
        max_length=2,
        choices=PreferredLanguageChoices.choices,
        default=PreferredLanguageChoices.OTHER,
        null=True,
    )
    birth_date: Field = models.DateField(
        "Birth date", null=True, auto_now_add=False
    )
    created_at: Field = models.DateTimeField(
        "Creation date", auto_now_add=True
    )
    updated_at: Field = models.DateTimeField("Update date", auto_now=True)

    def __str__(self) -> str:
        return f"User ({self.user_id}) profile ({self.pk})"

    def is_adult(self) -> bool:
        if not self.birth_date:
            return None
        adultness: datetime = datetime.now() - relativedelta(years=18)
        birthday: datetime = datetime.strptime(
            str(self.birth_date), "%Y-%m-%d"
        )
        return birthday < adultness


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender: View,
    instance: Model,
    reset_password_token: Model,
    *args: tuple,
    **kwargs: dict,
) -> None:
    from Emails.utils import send_email

    send_email("reset_password", reset_password_token)
