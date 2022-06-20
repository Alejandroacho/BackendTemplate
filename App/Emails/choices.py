from django.db import models


class CommentType(models.TextChoices):
    SUGGESTION = 'SUGGESTION'
    BUG = 'BUG'
    ERROR = 'ERROR'
    OTHER = 'OTHER'
