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
		elif self.status == 'interim':
			return 480

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

	def is_interim(self):
		return self.status == 'interim'

class Shift:
	def __init__(self, id, planning_id, user_id, start_date):
		self.id = id
		self.planning_id = planning_id
		self.user_id = user_id
		self.start_date = datetime.strptime(start_date, '%Y-%m-%d')

	def is_weekend(self):
		return self.start_date.strftime("%A") == "Saturday" or self.start_date.strftime("%A") == "Sunday"

class Commission:
	def __init__(self, workers):
		self.workers = workers

	def number_of_interim_shifts(self):
		interim_workers = []

		for worker in self.workers:
			if worker.is_interim():
				interim_workers.append(worker.shifts)
		
		return len(interim_workers[0])

	def pdg_fee(self):
		return self.interim_fee() + self.other_workers_fee()

	def interim_fee(self):
		return self.number_of_interim_shifts() * 80

	def other_workers_fee(self):
		sum = 0
		for worker in self.workers:
			sum += worker.total_price() * 0.05

		return sum

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

commission = Commission(workers)
result = { "workers": [{ "id": worker.id, "price": worker.total_price() } for worker in workers], "commission": { "pdg_fee": commission.pdg_fee(), "interim_shifts": commission.number_of_interim_shifts() } }

with open('output.json', 'w') as outfile:
	json.dump(result, outfile, indent=2, sort_keys=True)
