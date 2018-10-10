import sys
import os

import django
from django.contrib.auth import get_user_model

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(pwd))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drfproject.settings")

django.setup()

User = get_user_model()
users = []
for i in range(1, 11):
    users.append('admin%s' % i)

for user in users:
    User.objects.create_user(username=user, password=user)
