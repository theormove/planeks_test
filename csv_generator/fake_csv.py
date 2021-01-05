from .models import DataSet, DataSchema, DataSchemaColumn
from django.conf import settings
import random
import time
from celery import shared_task
import csv

dummy_data = {
				'Full name':['Ivan Ivanov', 'Pavel Durov','Elon Musk'],
				'Job':['python dev','hr','devops','teacher'],
				'Email':['ivan@gmail.com','pasha@gmail.com','elon@ukr.net'],
				'Domain name':['google.com','pomidorov.net','anime.io'],
				'Company name':['Google','Facebook','Amazon'],
				'Words':['Hello','today','was','nice','running','I'],
				'Address':['Peremogy ave 67','Shevchenka street 6','Lviv'],
				}
def fake_csv(row_number, schema_id, set_id):
	columns = DataSchemaColumn.objects.filter(parent=schema_id)
	columns_main = {}
	for column in columns:
		columns_main[str(column.order)] = [column.name, column.column_type]
		if column.range_supported:
			columns_main[str(column.order)].append(str(column.start_value))
			columns_main[str(column.order)].append(str(column.end_value))
	sorted_keys = sorted(columns_main.keys())
	header = []
	types = []
	for key in sorted_keys:
		header.append(columns_main[key][0])
		if columns_main[key][1] in ['Integer','Text']:
			types.append(columns_main[key][1]+'_'+columns_main[key][2]+'_'+columns_main[key][3])
		else:			
			types.append(columns_main[key][1])
	dummy_data = {
				'first_name':['Ivan', 'Pavel','Elon','Taras','Alexander'],
				'last_name':['Ivanov', 'Durov','Musk','Shevchenko','Makedonskiy'],
				'Job':['python dev','hr','devops','teacher', 'cyberathlete'],
				'Email':['ivan@gmail.com','pasha@gmail.com','elon@ukr.net','rybka.vika@gmail.com'],
				'Domain name':['google.com','pomidorov.net','anime.io', 'something.funny'],
				'Company name':['Google','Facebook','Amazon','Kyivstar'],
				'Words':['Hello','today','was','nice','running','I','maybe','thank','you','did','well'],
				'Address':['Peremogy ave 67','Shevchenka street 6','Lviv','New York','Washington'],
				}
	schema = DataSchema.objects.filter(id = schema_id).first()
	chars = [schema.column_separator, schema.string_character]			
	task = random_csv.delay(types,header,row_number,dummy_data,set_id,chars)
	return task.task_id			


@shared_task(bind=True)
def random_csv(self, columns, header, row_number, dummy_data, set_id, chars):
	with open(settings.MEDIA_ROOT + '/data_set_{}.csv'.format(set_id), 'w') as csvfile:
		writer = csv.writer(csvfile, delimiter = chars[0], quotechar = chars[1])
		writer.writerow(header)
		for i in range(int(row_number)):
			row = []
			for column in columns:
				if column in dummy_data.keys():
					row.append(random.choice(dummy_data[column]))
				elif column == 'Phone number':
					row.append(random.randrange(10**9,10**10))
				elif column == 'Full name':
					row.append(random.choice(dummy_data['first_name']) + " " + random.choice(dummy_data['last_name']))	
				elif column == 'Date':
					day = str(random.randrange(1,30))
					month = str(random.randrange(1,12))
					year = str(random.randrange(1970,2020))
					row.append('{}/{}/{}'.format(day,month,year))	
				elif column.split('_')[0] == 'Integer':
					row.append(random.randrange(int(column.split('_')[1]),int(column.split('_')[2])))
				elif column.split('_')[0] == 'Text':
					text = ''
					for i in range(random.randrange(int(column.split('_')[1]),int(column.split('_')[2]))):
						sentence = ''
						for word in dummy_data['Words']:
							sentence += random.choice(dummy_data['Words'])
							sentence += " "
						sentence += ". "
						text += sentence
					row.append(text)	

				
			writer.writerow(row)
		data_set = DataSet.objects.filter(id = set_id).first()
		data_set.file = '/data_set_{}.csv'.format(set_id)
		data_set.status = 'SUCCESS'
		data_set.save()					
			