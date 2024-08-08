from django.db import models
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
import re
from django.contrib.auth import get_user_model


email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@(?:[A-Z0-9-]+\.)+[A-Z]{2,6}$', re.IGNORECASE)

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None):
        print(email,password,'password')
        User = get_user_model()
        if email_re.search(email):
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
        
    def get_user(self, user_id):
       try:
          return User.objects.get(pk=user_id)
       except User.DoesNotExist:
          return None