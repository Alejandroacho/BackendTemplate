from django.db import models


class GenderChoices(models.TextChoices):
    FEMALE: tuple = ("F", "Female")
    MALE: tuple = ("M", "Male")
    NON_BINARY: tuple = ("N", "Non-binary")
    NOT_SAID: tuple = ("P", "Prefer not to say")


class PreferredLanguageChoices(models.TextChoices):
    ENGLISH: tuple = ("EN", "English")
    SPANISH: tuple = ("ES", "Spanish")
    FRENCH: tuple = ("FR", "French")
    OTHER: tuple = ("OT", "Other")
