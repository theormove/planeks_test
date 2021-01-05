from django.contrib import admin
from .models import DataSchema, DataSchemaColumn, DataSet

admin.site.register(DataSchema)
admin.site.register(DataSchemaColumn)
admin.site.register(DataSet)
# Register your models here.
