from django.db import models

class Chrono(models.Model):
    added = models.IntegerField(blank=True)
    sold = models.IntegerField(blank=True)
    updated = models.IntegerField(blank=True)
    class Meta:
        ordering = ['id']
