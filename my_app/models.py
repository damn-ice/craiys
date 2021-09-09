from django.db import models


class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField("created", auto_now=True)

    class Meta:
        verbose_name_plural = "searches"

    def __str__(self):
        return self.search[:50]
# Create your models here.
