from django.shortcuts import render, redirect
from .forms import  DataSchemaColumnForm
from .models import DataSchema, DataSchemaColumn, DataSet
from .fake_csv import fake_csv
from django_celery_results.models import TaskResult

def progress(request,slug):
	task = TaskResult.objects.filter(task_id = slug).first()
	data = {'state':task.status,}
	return render(request, 'csv_generator/progress.html', data)

def forbidden(request):
	return render(request, 'csv_generator/forbidden.html')	

def data_schemas(request):
	if request.user.is_authenticated:
		if request.method == "POST":
			DataSchema.objects.filter(id = request.POST.get('del')).first().delete()
		schemas = DataSchema.objects.filter(owner = request.user.id)
		i = 0
		numeration = []
		try: 
			for obj in schemas:
				i += 1
				obj.pos = i
		except:
			pass		
		data = {'schemas': schemas,
		} 
		return render(request, 'csv_generator/data_schemas.html', data)
	else:
		return redirect('login')

def data_schema(request, pk):
	if request.user.is_authenticated:
		if DataSchema.objects.filter(id=pk).first().owner == request.user:
			if request.method == "POST":
				if request.POST.get('form') == 'new':
					if DataSchemaColumnForm(request.POST).is_valid():
						range_sup = False
						if request.POST.get('column_type') in ['Integer','Text']:
							range_sup = True
						column = DataSchemaColumn(name =request.POST.get('name'), column_type = request.POST.get('column_type'), order = request.POST.get('order'), range_supported =range_sup, parent = DataSchema.objects.filter(id=pk).first())
						column.save()
				elif request.POST.get('form') == 'old':
					schema = DataSchema.objects.filter(id=pk).first()
					schema.name = request.POST.get('schema_name') 
					schema.column_separator = request.POST.get('column_separator')
					schema.string_character = request.POST.get('string_character')
					schema.save()
					for column in DataSchemaColumn.objects.filter(parent=pk):
						str_id = str(column.id)
						if column.range_supported:
							column.start_value = request.POST.get('start'+str_id)
							column.end_value = request.POST.get('end'+str_id)
						column.name = request.POST.get('name'+str_id)
						column.column_type = request.POST.get('type'+str_id)
						column.order = request.POST.get('order'+str_id)
						try:
							column.save()
						except:
							pass	
					return redirect('data-schemas')
				else:
					with open('form.txt', 'w') as f:
						f.write(str(request.POST))
					DataSchemaColumn.objects.filter(id = request.POST.get('form').replace('del','')).first().delete()				
			data = {
					'schema':DataSchema.objects.filter(id=pk).first(),
					'columns':DataSchemaColumn.objects.filter(parent=pk),
					'options':['Full name','Job','Email','Domain name','Phone number','Company name','Text','Integer','Address','Date'],
					'options2':[',','-',';'],
					'options3':["'",'"','|'],
					}
			return render(request, 'csv_generator/data_schema.html', data)
		else:
			return redirect('forbidden')	
	else:
		return redirect('login')

def new_data_schema(request):
	if request.user.is_authenticated:
		new_schema = DataSchema(owner = request.user, name = "New Schema", column_separator = ',', string_character = '"')
		if request.method == "POST":
			if request.POST.get('form') == 'new':
				if DataSchemaColumnForm(request.POST).is_valid():
					new_schema.save()
					range_sup = False
					if request.POST.get('column_type') in ['Integer','Text']:
						range_sup = True
					column = DataSchemaColumn(name =request.POST.get('name'), column_type = request.POST.get('column_type'), range_supported =range_sup, order = request.POST.get('order'), parent = new_schema)
					column.save()
					new_schema.name = request.POST.get('schema_name') 
					new_schema.column_separator = request.POST.get('column_separator')
					new_schema.string_character = request.POST.get('string_character')
					new_schema.save()
					return redirect('data-schema', pk = new_schema.id)	
#		with open('form.txt', 'w') as f:
#					f.write(str(new_schema.name))
		data = {
				'schema':new_schema,
				'columns':{},
				'options':['Full name','Job','Email','Domain name','Phone number','Company name','Text','Integer','Address','Date'],
				'options2':[',','-',';'],
				'options3':["'",'"','|'],
				}
		return render(request, 'csv_generator/new_data_schema.html', data)
	else:
		return redirect('login')

def data_sets(request, pk):
	if DataSchema.objects.filter(id=pk).first().owner == request.user:
		if request.method == "POST":
			data = {'sets':DataSet.objects.filter(parent = pk),
					'name':DataSchema.objects.filter(id = pk).first().name,
					'last_object':''}
			if request.POST.get('rows'):
				data_set = DataSet(status='PROCESSING', parent = DataSchema.objects.filter(id = pk).first(), rows = request.POST.get('rows'))
				data_set.save()
				data_set.task_id = fake_csv(request.POST.get('rows'), pk, data_set.id)
				data_set.save()	
				data = {'sets':DataSet.objects.filter(parent = pk),
						'name':DataSchema.objects.filter(id = pk).first().name,
						'last_object':data_set}
		else:
			data = {'sets':DataSet.objects.filter(parent = pk),
					'name':DataSchema.objects.filter(id = pk).first().name,
					'last_object':''}			
		return render(request, 'csv_generator/data_sets.html', data)
	else:
		return redirect('forbidden')
							