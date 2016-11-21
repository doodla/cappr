from __future__ import unicode_literals

from django.db import models
from django.db.models import CharField


class Color(models.Model):
    dominant = CharField(max_length=255, default="")
    background = CharField(max_length=255, default="")
    accent = CharField(max_length=255, default="")

    class Meta:
        abstract = True


class RGB(Color):
    pass


class HEX(Color):
    pass


class Cap(models.Model):
    name = CharField(max_length=255, default="")
    SKU = CharField(primary_key=True, max_length=255)
    type = CharField(max_length=255, default="")
    audience = CharField(max_length=255, default="")
    url = CharField(max_length=255, default="")
    price = CharField(max_length=255, default="")
    detail = CharField(max_length=255, default="")
    team = CharField(max_length=255, default="", name='team')
    rgb = models.ForeignKey(RGB, on_delete=models.CASCADE, null=True, blank=True)
    hex = models.ForeignKey(HEX, on_delete=models.CASCADE, null=True, blank=True)
    png = models.ImageField(upload_to='pngs/', null=True, blank=True)

    def image_url(self, typeof, direction):
        options = {'THUMBNAIL': ('80', '60'), 'COVER': ('400', '300'), 'HIGHLIGHT': ('800', '600'),
                   'HIGH-RES': ('1600', '1200')}
        facing = {'LEFT': '2', 'CENTER': '3', 'RIGHT': '4', 'BACK': '6'}

        return 'http://lf.lids.com/hwl?set=sku[' + self.SKU + '],c[' + facing[
            direction] + '],w[' + options[typeof][0] + '],h[' + options[typeof][1] + ']&load=url[file:product]'

    @property
    def cover_img(self):
        return 'http://lf.lids.com/hwl?set=sku[' + self.SKU + '],c[3],w[400],h[300]&load=url[file:product]'
