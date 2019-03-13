from django.contrib.auth.models import User
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import get_access_token_model, get_application_model
from django.contrib.auth import get_user_model
from django.utils import timezone

Application = get_application_model()
AccessToken = get_access_token_model()
UserModel = get_user_model()


def create_test_user(cls):
    user = User.objects.create(username='testuser')
    user.set_password('12345')
    user.save()
    cls.user = user


def create_second_test_user(cls):
    user = User.objects.create(username='second_user')
    user.set_password('12345')
    user.save()
    cls.second_user = user


def create_auth(cls, user):
    oauth2_settings._SCOPES = ["read", "write", "scope1", "scope2", "resource1"]

    test_user = user

    application = Application.objects.create(name="Test Application",
                                             redirect_uris="http://localhost http://example.com http://example.org",
                                             user=test_user, client_type=Application.CLIENT_CONFIDENTIAL,
                                             authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,)

    access_token = AccessToken.objects.create(user=test_user, scope="read write",
                                              expires=timezone.now() + timezone.timedelta(seconds=300),
                                              token="secret-access-token-key", application=application)

    # read or write as per your choice
    access_token.scope = "read"
    access_token.save()

    # correct token and correct scope
    cls.auth = "Bearer {0}".format(access_token.token)
