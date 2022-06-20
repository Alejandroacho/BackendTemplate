import pytest
from django.core import mail
from rest_framework.test import APIClient

from Emails.choices import CommentType
from Emails.factories.suggestion import SuggestionEmailFactory
from Emails.models.models import Suggestion
from Users.fakers.user import AdminFaker
from Users.fakers.user import UserFaker
from Users.fakers.user import VerifiedUserFaker


@pytest.fixture(scope='function')
def client():
    return APIClient()


BASE_ENDPOINT = '/api/suggestions'


@pytest.mark.django_db
class TestSubmitSuggestionViews:

    ACTION = 'submit'
    ENDPOINT = f'{BASE_ENDPOINT}/{ACTION}/'

    def test_suggestion_fails_as_unauthenticate_user(self, client):
        assert len(mail.outbox) == 0
        data = {'type': 'Error', 'content': 'Error found'}
        response = client.post(self.ENDPOINT, data, format='json')
        assert response.status_code == 401
        assert len(mail.outbox) == 0

    def test_suggestion_creates_email_as_authenticate_user(self, client):
        normal_user = VerifiedUserFaker()
        email_count = Suggestion.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        type = CommentType.ERROR.value
        data = {'type': type, 'content': 'Error found'}
        client.force_authenticate(user=normal_user)
        response = client.post(self.ENDPOINT, data, format='json')
        email_count = Suggestion.objects.all().count()
        expected_header = f'ERROR from user with id: {normal_user.id}'
        assert response.status_code == 201
        assert True == response.data['was_sent']
        assert 'ERROR' == response.data['subject']
        assert expected_header == response.data['header']
        block = Suggestion.objects.first().blocks.first()
        assert [block.id] == response.data['blocks']
        assert 'Error found' == response.data['content']
        assert len(mail.outbox) == 1
        assert email_count == 1

    def test_suggestion_fails_as_authenticate_user_because_wrong_type(
        self, client
    ):
        normal_user = VerifiedUserFaker()
        email_count = Suggestion.objects.all().count()
        assert len(mail.outbox) == 0
        assert email_count == 0
        data = {'type': 'Wrong', 'content': 'Error found'}
        client.force_authenticate(user=normal_user)
        response = client.post(self.ENDPOINT, data, format='json')
        email_count = Suggestion.objects.all().count()
        expected_error_message = 'Type not allowed'
        assert response.status_code == 400
        assert expected_error_message in response.data['detail']
        assert len(mail.outbox) == 0
        assert email_count == 0


@pytest.mark.django_db
class TestReadSuggestionViews:

    ACTION = 'read'

    def test_read_suggestion_fails_as_unauthenticate_user(self, client):
        user = UserFaker()
        type = CommentType.ERROR.value
        content = 'Error found'
        suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        pk = suggestion.pk
        url = f'{BASE_ENDPOINT}/{pk}/{self.ACTION}/'
        response = client.post(url, format='json')
        assert response.status_code == 401

    def test_read_suggestion_fails_as_unverified_user(self, client):
        user = UserFaker()
        client.force_authenticate(user=user)
        type = CommentType.ERROR.value
        content = 'Error found'
        suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        pk = suggestion.pk
        url = f'{BASE_ENDPOINT}/{pk}/{self.ACTION}/'
        response = client.post(url, format='json')
        assert response.status_code == 403

    def test_suggestion_is_read_as_admin(self, client):
        user = AdminFaker()
        client.force_authenticate(user=user)
        type = CommentType.ERROR.value
        content = 'Error found'
        suggestion = SuggestionEmailFactory(
            type=type, content=content, user=user
        )
        assert suggestion.was_read == False
        pk = suggestion.pk
        url = f'{BASE_ENDPOINT}/{pk}/{self.ACTION}/'
        response = client.post(url, format='json')
        assert response.status_code == 200
        suggestion.refresh_from_db()
        assert suggestion.was_read == True


@pytest.mark.django_db
class TestUserSuggestionViews:

    ACTION = 'user'

    def test_list_user_suggestion_without_user_id_fails_as_unauthenticate(
        self, client
    ):
        response = client.get(f'{BASE_ENDPOINT}/{self.ACTION}/')
        assert response.status_code == 401

    def test_list_user_suggestion_with_user_id_fails_as_unauthenticate(
        self, client
    ):
        user = UserFaker()
        response = client.get(f'{BASE_ENDPOINT}/{self.ACTION}/?user={user.id}')
        assert response.status_code == 401

    def test_list_user_suggestion_with_user_id_fails_as_other_user(
        self, client
    ):
        user = UserFaker()
        client.force_authenticate(user=user)
        other_user = UserFaker()
        type = CommentType.ERROR.value
        content = 'Error found'
        SuggestionEmailFactory(type=type, content=content, user=other_user)
        url = f'{BASE_ENDPOINT}/{self.ACTION}/?user_id={other_user.id}'
        response = client.get(url)
        assert response.status_code == 403

    def test_list_user_suggestion_with_user_id_returns_suggestions_as_admin(
        self, client
    ):
        admin = AdminFaker()
        client.force_authenticate(user=admin)
        user = UserFaker()
        type = CommentType.ERROR.value
        content = 'Error found'
        SuggestionEmailFactory(type=type, content=content, user=user)
        url = f'{BASE_ENDPOINT}/{self.ACTION}/?user_id={user.id}'
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['count'] == Suggestion.objects.count()

    def test_list_user_suggestion_with_out_user_id_returns_suggestions_as_user(
        self, client
    ):
        user = UserFaker()
        client.force_authenticate(user=user)
        type = CommentType.ERROR.value
        content = 'Error found'
        SuggestionEmailFactory(type=type, content=content, user=user)
        url = f'{BASE_ENDPOINT}/{self.ACTION}/'
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['count'] == Suggestion.objects.count()

    def test_list_user_suggestion_with_user_id_returns_suggestions_as_user(
        self, client
    ):
        user = UserFaker()
        client.force_authenticate(user=user)
        type = CommentType.ERROR.value
        content = 'Error found'
        SuggestionEmailFactory(type=type, content=content, user=user)
        url = f'{BASE_ENDPOINT}/{self.ACTION}/?user_id={user.id}'
        response = client.get(url)
        assert response.status_code == 200
        assert len(response.data['results']) == 1
        assert response.data['count'] == Suggestion.objects.count()
