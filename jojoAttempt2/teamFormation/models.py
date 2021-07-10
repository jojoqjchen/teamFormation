from django.db import models
from django.core.validators import FileExtensionValidator

# Create your models here.
#VALIDATOR DOES NOT WORK YET
class csvUpload(models.Model):
    csvFile = models.FileField(validators = [FileExtensionValidator(allowed_extensions=['csv'])])

class pickCols(models.Model):
    similarCols = models.IntegerField(blank=True, null=True)
    diffCols = models.IntegerField(blank=True, null=True)
