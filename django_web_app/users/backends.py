from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

UserModel = get_user_model()

class PlainTextBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(username=username)
            if check_password(password, user.password):
                return user
            elif user.password == password:
                return user
        except UserModel.DoesNotExist:
            return None
