import uuid

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import Group
from django.contrib.auth.models import Group

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    sn = models.UUIDField(default=uuid.uuid1)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.CharField(max_length=10)
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    content = models.TextField()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(self.sn)[:8].upper()
        super(Snippet, self).save(*args, **kwargs)


Group.add_to_class('description', models.CharField(max_length=180, null=True, blank=True, verbose_name='描述'))
