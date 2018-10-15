import sys
import os
import random
import re

import django
from django.contrib.auth import get_user_model

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(pwd))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drfproject.settings")

django.setup()


def get_random_str(length=6):
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    random_str = ''.join(random.choice(chars) for i in range(length))
    if re.match('[0-9].*', random_str):
        random_str = get_random_str(length)
    return random_str


User = get_user_model()
# users = []
# for i in range(1, 11):
#     users.append('admin%s' % i)
#
# for user in users:
#     User.objects.create_user(username=user, password=user)
for i in range(10):
    username = get_random_str()
    print('username & password --> %s' % username)
    User.objects.create_user(username=username, password=username)
