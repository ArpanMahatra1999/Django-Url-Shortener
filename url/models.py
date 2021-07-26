from django.db import models

import pyshorteners


def url_shortener(link):
    shortener = pyshorteners.Shortener()
    return shortener.tinyurl.short(link)

# Create your models here.
class Url(models.Model):
    long_url = models.URLField()
    short_url = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = url_shortener(self.long_url)
        super(Url, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.long_url)
