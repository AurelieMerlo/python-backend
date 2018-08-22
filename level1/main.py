import json

class Worker:
	def __init__(self, id, first_name, price_per_shift):
		self.id = id
		self.first_name = first_name
		self.price_per_shift = price_per_shift
		self.shifts = []

	def total_price(self):
		return self.price_per_shift * len(self.shifts)

class Shift:
	def __init__(self, id, planning_id, user_id, start_date):
		self.id = id
		self.planning_id = planning_id
		self.user_id = user_id
		self.start_date = start_date

with open('data.json') as file:
	data = json.load(file)

	workers = []
	for worker in data['workers']:
		workers.append(Worker(worker['id'], worker['first_name'], worker['price_per_shift']))

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
