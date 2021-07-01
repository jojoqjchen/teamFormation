from django.db import models
# from .validators import validate_file_extension
# import hashlib, random

# Create your models here.

#Step 1
class upload(models.Model):
    csvFile = models.FileField()
    def __str__(self):
        return self.csvFile
#Step 2
class size(models.Model):
    teamSize = models.IntegerField()
    def __str__(self):
        return self.teamSize
#Step 3
class characteristics(models.Model):
    characteristic = models.CharField(max_length=50)
    def __str__(self):
        return self.characteristic



# class Document(models.Model):
#     file = models.FileField(upload_to="documents/%Y/%m/%d", validators=[validate_file_extension])
# # Creates a unique session identification hashcode for each time a user starts the form
# def create_hash():
#     hash = hashlib.sha1()
#     hash.update(str(random.randint(0,sys.maxsize)).encode('utf-8'))
#     return hash.hexdigest
# class teams(models.Model):
#     #operational definitions
#     session_hash = models.CharField(max_length=40, unique=True)
#     stage = models.CharField(max_length=10, default=constants.STAGE_1)
#     #stage 1: upload csv 
#     csv = models.FileField(upload_to="media")
#     #stage 2: enter team size
#     teamSize = models.IntegerField()
#     #stage 3: choose which columns 

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         #checks for the small possibility that the hash code generated has already been seen 
#         if not self.session_hash:
#             while True:
#                 session_hash = create_hash()
#                 if teams.objects.filter(session_hash=session_hash).count() == 0:
#                     self.session_hash = session_hash
#                     break 

#     #returns the correct fields depending on the stage 
#     @staticmethod
#     def get_fields(stage):
#         fields = ['stage'] #required 
#         if stage == constants.STAGE_1:
#             fields.extend(['csv']) 
#         elif stage == constants.STAGE_2:
#             fields.extend(['teamSize'])
#         return fields 

