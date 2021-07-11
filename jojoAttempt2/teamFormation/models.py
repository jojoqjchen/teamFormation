from django.db import models
from . import validators

# Create your models here.
class csvUpload(models.Model):
    csvFile = models.FileField(validators = [validators.validate_file_extension], upload_to='media/media')

    def __str__(self):
        return self.csvFile

class pickCols(models.Model):
    pass

class teamSize(models.Model):
    size = models.IntegerField(blank=True, null=True)
