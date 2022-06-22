from django.db import models


class CommentType(models.TextChoices):
    SUGGESTION: str = "SUGGESTION"
    BUG: str = "BUG"
    ERROR: str = "ERROR"
    OTHER: str = "OTHER"
