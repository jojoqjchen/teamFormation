from django.db import models
# Create your models here.
from . import validators

class Upload(models.Model):
    csvFile = models.FileField(validators = [validators.validate_file_extension],upload_to='surveys/csv/')
    def __str__(self):
        return self.csvFile
