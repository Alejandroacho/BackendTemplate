from django.db import models


class CommentType(models.TextChoices):
    SUGGESTION: str = "SUGGESTION"
    BUG: str = "BUG"
    ERROR: str = "ERROR"
    OTHER: str = "OTHER"


class EmailAffair(models.TextChoices):
    NOTIFICATION: str = "NOTIFICATION"
    PROMOTION: str = "PROMOTION"
    GENERAL: str = "GENERAL"
    SETTINGS: str = "SETTINGS"
    INVOICE: str = "INVOICE"
    SUGGESTION: str = "SUGGESTION"
