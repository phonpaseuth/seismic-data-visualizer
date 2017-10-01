from django.db import models
from rest_framework import permissions

# Create your models here.
class Log(models.Model):
    permission_classes = (permissions.IsAuthenticated,)
    data_id = models.CharField(max_length=256)  # what data is accessed
    access_date = models.DateTimeField('date accessed') # what time
    action = models.CharField(max_length=100)   # what action to the data (POST/GET)
    user_id = models.CharField(max_length=100)  # who accessed the data
    command = models.CharField(max_length=512)  # command to access the data

    def __str__(self):
        return "Data: " + self.data_id + ", " + self.access_date.strftime("%m/%d/%Y %H:%M:S") + ", " + self.action + ", " + self.user_id + ", " + self.command


class DataInfo(models.Model):
    data_id = models.CharField(max_length=256)
    data_type = models.CharField(max_length=256)  #seismic, csv ...
    data_storage = models.CharField(max_length=256) # file, database, No-SQL database...
    data_location = models.CharField(max_length=512)  # file path, database info ..
    owner = models.CharField(max_length=256)  # data owner

    def __str__(self):
        return "Data: " + self.data_id + ", " + self.data_type + ", " + self.data_storage + ", " + self.data_location
