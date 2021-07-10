from django.db import models
# Create your models here.
from . import validators
from django.contrib.auth.models import User


class Upload(models.Model):
    csvFile = models.FileField(validators = [validators.validate_file_extension],upload_to='surveys/csv/')
    timestamp = models.DateTimeField(auto_now_add = True, null=True)
    related_user = models.ForeignKey(User, on_delete = models.CASCADE, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.csvFile
