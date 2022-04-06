from django.db import models


class GenderChoices(models.TextChoices):
    FEMALE = ('F', 'Female')
    MALE = ('M', 'Male')
    NON_BINARY = ('N', 'Non-binary')
    NOT_SAID = ('P', 'Prefer not to say')