import pytest
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestUsersManagers:
    def test_create_user_successfully(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='normaluser@test.com',
            first_name='test_name',
            last_name='test_last_name',
            password='test_password',
        )
        assert user.email == 'normaluser@test.com'
        assert user.is_active == True
        assert user.username == None

    def test_create_user_fails_without_data(self):
        User = get_user_model()
        with pytest.raises(TypeError):
            User.objects.create_user()

    def test_create_user_fails_with_email_and_without_password(self):
        User = get_user_model()
        with pytest.raises(TypeError):
            User.objects.create_user(email='email@test.com', password='')

    def test_create_user_fails_without_email_with_all_data(self):
        User = get_user_model()
        with pytest.raises(ValueError):
            User.objects.create_user(
                email=None,
                first_name='test_name',
                last_name='test_last_name',
                password='test_password',
            )

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            email='super@user.com',
            first_name='test_name',
            last_name='test_last_name',
            password='test_password',
        )
        assert admin_user.email == 'super@user.com'
        assert admin_user.is_verified == True
        assert admin_user.username == None

    def test_create_superuser_fails_without_data(self):
        User = get_user_model()
        with pytest.raises(TypeError):
            User.objects.create_superuser()

    def test_create_superuser_fails_with_email_and_without_password(self):
        User = get_user_model()
        with pytest.raises(TypeError):
            User.objects.create_superuser(
                email='adminemail@test.com', password=""
            )

    def test_create_superuser_fails_with_email_without_password(self):
        User = get_user_model()
        with pytest.raises(TypeError):
            User.objects.create_superuser(email='', password='foo')
