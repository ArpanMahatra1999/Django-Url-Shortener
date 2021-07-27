from django.db import models

from url.shorteners import shortener

# Create your models here.
class Url(models.Model):
    long_url = models.URLField(verbose_name='Type Url Here')
    token = models.CharField(max_length=255, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = shortener().issue_token()
        super(Url, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.long_url)
