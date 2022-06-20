import pytest
from django.db.utils import IntegrityError
from mock import MagicMock
from mock import PropertyMock
from rest_framework.serializers import ValidationError

from Users.factories.profile import ProfileFactory
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker
from Users.serializers import ProfileSerializer


@pytest.mark.django_db
class TestProfileSerializer:
    def test_data_serialized_from_profile(self):
        user = VerifiedUserFaker()
        profile = user.profile
        expected_data = {
            'id': profile.id,
            'user_id': profile.user_id,
            'nickname': profile.nickname,
            'bio': profile.bio,
            'image': profile.image,
            'gender': profile.gender,
            'preferred_language': profile.preferred_language,
            'birth_date': profile.birth_date,
            'is_adult': profile.is_adult(),
        }
        actual_data = ProfileSerializer(profile).data
        assert actual_data == expected_data

    def test_update(self):
        user = VerifiedUserFaker()
        profile = user.profile
        serializer = ProfileSerializer()
        data = {
            'nickname': 'New nickname',
            'bio': 'New bio',
            'gender': 'N',
            'preferred_language': 'ES',
        }
        serializer.update(profile, data)
        profile.refresh_from_db()
        assert profile.nickname == data['nickname']
        assert profile.bio == data['bio']
        assert profile.gender == data['gender']
        assert profile.preferred_language == data['preferred_language']

    def test_create(self):
        user = UserFaker()
        serializer = ProfileSerializer()
        data = {
            'user_id': user.id,
        }
        profile = serializer.create(data)
        assert profile.user_id == data['user_id'] == user.id

    def test_create_fails_with_nickname_taken(self):
        first_user = VerifiedUserFaker()
        first_profile = first_user.profile
        first_profile.nickname = 'Nickname taken'
        first_profile.save()
        admin = AdminFaker()
        context = MagicMock()
        mocked_requester = PropertyMock(return_value=admin)
        type(context).user = mocked_requester
        data = {'nickname': first_profile.nickname}
        serializer = ProfileSerializer(context=context, data=data)
        with pytest.raises(IntegrityError):
            serializer.create(data)

    def test_s_valid_fails_with_nickname_taken(self):
        first_user = VerifiedUserFaker()
        first_profile = first_user.profile
        first_profile.nickname = 'Nickname taken'
        first_profile.save()
        admin = AdminFaker()
        context = MagicMock()
        mocked_requester = PropertyMock(return_value=admin)
        type(context).user = mocked_requester
        data = {'nickname': first_profile.nickname}
        serializer = ProfileSerializer(context=context, data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(data)
