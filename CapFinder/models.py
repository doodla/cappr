from __future__ import unicode_literals

from django.db import models
from django.db.models import CharField
from django.db.models import IntegerField


class Cap(models.Model):
    name = CharField(max_length=255, default="")
    picture = CharField(max_length=255, default="")

    hexDominantColor = CharField(max_length=255, default="")
    hexBackgroundColor = CharField(max_length=255, default="")
    hexAccentColor = CharField(max_length=255, default="")

    rgbDominantColor = CharField(max_length=255, default="")
    rgbBackgroundColor = CharField(max_length=255, default="")
    rgbAccentColor = CharField(max_length=255, default="")

    url = CharField(max_length=255, default="")
    price = IntegerField(default=0)

    emotion = CharField(max_length=255, default='Happy')
