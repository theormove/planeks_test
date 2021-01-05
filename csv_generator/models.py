from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class DataSchema(models.Model):
    name = models.CharField(max_length=100)
    column_separator = models.CharField(max_length=10)
    string_character = models.CharField(max_length=10)
    last_change = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

class DataSchemaColumn(models.Model):
	parent = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	column_type = models.CharField(max_length=100)
	range_supported = models.BooleanField(default = False)
	start_value = models.IntegerField(blank = True, default = 1) 
	end_value = models.IntegerField(blank = True, default = 3) 
	order = models.IntegerField()

class DataSet(models.Model):
	parent = models.ForeignKey(DataSchema, on_delete=models.CASCADE)
	date = 	models.DateTimeField(default=timezone.now)
	status = models.CharField(max_length=20)
	rows = models.IntegerField(default=10)
	task_id = models.CharField(max_length=100, default='')
	file = models.FileField(default="error.csv", upload_to = '')