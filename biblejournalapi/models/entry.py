from django.db import models
from django.db.models.deletion import CASCADE

class Entry(models.Model):
    reader = models.ForeignKey("Reader", on_delete=CASCADE)
    hear = models.CharField(max_length=500)
    engage = models.CharField(max_length=500)
    apply = models.CharField(max_length=500)
    respond = models.CharField(max_length=500)
    date = models.DateField()
    refrence = models.CharField(max_length=20)