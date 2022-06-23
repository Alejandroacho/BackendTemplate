from django.db.models import Field
from django.db.models import Model
from Emails.models.models import Suggestion
from rest_framework import serializers
from rest_framework.relations import RelatedField


class SuggestionEmailSerializer(serializers.Serializer):
    """
    Suggestion serializer
    """

    id: Field = serializers.IntegerField()
    user_id: Field = serializers.IntegerField()
    was_sent: Field = serializers.BooleanField()
    was_read: Field = serializers.BooleanField()
    subject: Field = serializers.CharField()
    header: Field = serializers.CharField()
    blocks: RelatedField = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="id"
    )
    content: Field = serializers.CharField(source="blocks.first.content")

    class Meta:
        model: Model = Suggestion
