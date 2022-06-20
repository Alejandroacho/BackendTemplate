from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers

from Emails.models.models import Suggestion


class SuggestionEmailSerializer(serializers.Serializer):
    """
    Suggestion serializer
    """

    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    was_sent = serializers.BooleanField()
    was_read = serializers.BooleanField()
    subject = serializers.CharField()
    header = serializers.CharField()
    blocks = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field='id'
    )
    content = serializers.CharField(source='blocks.first.content')

    class Meta:
        model = Suggestion
