from django.db import models
from . import validators
from django.contrib.auth.models import User


# Create your models here.
class csvUpload(models.Model):
    csvFile = models.FileField(validators = [validators.validate_file_extension], upload_to='media/media')

    def __str__(self):
        return self.csvFile

class pickCols(models.Model):
    pass

class teamSize(models.Model):
    size = models.IntegerField(blank=True, null=True)

class numberOfDownloads(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    download = models.IntegerField()
