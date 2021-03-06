import json
from datetime import datetime

class Worker:
	def __init__(self, id, first_name, status):
		self.id = id
		self.first_name = first_name
		self.status = status
		self.shifts = []

	def price_per_status(self):
		if self.status == 'medic':
			return 270
		elif self.status == 'interne':
			return 126

	def total_price(self):
		return self.price_per_status() * self.number_of_shifts()

	def number_of_shifts(self):
		sum = 0
		for shift in self.shifts:
			if shift.is_weekend():
				sum += 2
			else:
				sum += 1
		return sum

class Shift:
	def __init__(self, id, planning_id, user_id, start_date):
		self.id = id
		self.planning_id = planning_id
		self.user_id = user_id
		self.start_date = datetime.strptime(start_date, '%Y-%m-%d')

	def is_weekend(self):
		return self.start_date.strftime("%A") == "Saturday" or self.start_date.strftime("%A") == "Sunday"

with open('data.json') as file:
	data = json.load(file)

	workers = []
	for worker in data['workers']:
		workers.append(Worker(worker['id'], worker['first_name'], worker['status']))

	shifts = []
	for shift in data['shifts']:
		shifts.append(Shift(shift['id'], shift['planning_id'], shift['user_id'], shift['start_date']))
	
for worker in workers:
	for shift in shifts:
		if worker.id == shift.user_id:
			worker.shifts.append(shift)

result = { "workers": [{ "id": worker.id, "price": worker.total_price() } for worker in workers] }

with open('output.json', 'w') as outfile:
	json.dump(result, outfile, indent=2, sort_keys=True)
