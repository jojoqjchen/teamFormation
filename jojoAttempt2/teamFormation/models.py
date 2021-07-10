from django.db import models

# Create your models here.
class csvUpload(models.Model):
    csvFile = models.FileField()

class pickCols(models.Model):
    pass
class teamSize(models.Model):
    size = models.IntegerField(blank=True, null=True)