# ~*~ coding:utf-8 ~*~

from main.models import User

class UserBasicBackend:
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class EmailBackend(UserBasicBackend):
    def authenticate(self, email=None, password=None):
        #If username is an email address, then try to pull it up
        user = None
        try:
            user = User.objects.get(email=email, is_active=True)
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        return None


class VerificationCodeBackend(UserBasicBackend):
    def authenticate(self, email=None, code=None):
        user = None
        try:
            user = User.objects.get(email=email, is_active=True)
            if user and user.verify(code):
                return user
        except User.DoesNotExist:
            return None

        return None
