#!/usr/bin/python

from random import random

class Person(object):
	
	def __init__(self, name, probability_in_on_any_day):
		self.name = name
		self.probability_in_on_any_day = probability_in_on_any_day
		
		self.times_cooked = 0
		self.times_eaten = 0
		self.last_cooked = -1
		self._times_between_cooking = []
		
		self._in_on_day = {}
	
	
	@property
	def times_between_cooking(self):
		return self._times_between_cooking[1:]
	
	
	def cooked(self, day):
		self._times_between_cooking.append(day - self.last_cooked)
		self.times_cooked += 1
		self.last_cooked = day
	
	
	def ate(self, day):
		self.times_eaten += 1
	
	
	def _random_in_today(self, day):
		return self._in_on_day.setdefault(day,
		                                  random() > self.probability_in_on_any_day)
	
	
	def can_eat_on_day(self, day):
		return self._random_in_today(day)
	
	
	def can_cook_on_day(self, day):
		return self._random_in_today(day)
	
	
	def __str__(self):
		return self.name



class James(Person):
	
	def can_cook_on_day(self, day):
		# Can't cook on Friday
		return Person.can_cook_on_day(self, day) and ((day % 7) != 4)
	
	def can_eat_on_day(self, day):
		# Can't eat on Friday
		return Person.can_eat_on_day(self, day) and( (day % 7) != 4)




class Jonathan(Person):
	
	def can_cook_on_day(self, day):
		# Can't cook on Tuesday
		return Person.can_cook_on_day(self, day) and ((day % 7) != 1)



def graph(_people, get_value, ordering):
	people = _people[:]
	people.sort(ordering)
	
	_max = max(people, key = (lambda p: get_value(p)))
	_min = min(people, key = (lambda p: get_value(p)))
	_avg = sum(get_value(p) for p in people) / len(people)
	
	print "Min: %s (%s)"%(_min.name, get_value(_min))
	print "Max: %s (%s)"%(_max.name, get_value(_max))
	print "Avg: %s"%_avg
	
	for person in people:
		print "%-10s %6s %s"%(person.name, get_value(person),
		                      "=" * int((get_value(person) * 60) / get_value(_max)))



def main(pick_cooker, days):
	people = [
		James("James",       0.1),
		Jonathan("Jonathan", 0.1),
		Person("Karl",       0.1),
		Person("Matt",       0.15),
		Person("Tom",        0.15),
	]
	
	day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
	
	for day, cook in pick_cooker(people, days):
		if cook is not None:
			cook.cooked(day)
			eaters = []
			for person in people:
				if person.can_eat_on_day(day):
					person.ate(day)
					eaters.append(person)
			if False:
				print "Day %2d, %s: %-10s cooked, %s ate."%(day, day_names[day%7], cook,
			                                       ", ".join(str(p) for p in eaters))
	
	print "--- Times Cooked -----------------------------------------------------"
	get_value = (lambda p: p.times_cooked)
	graph(people, get_value,
	              (lambda a, b: get_value(b) - get_value(a)))
	
	print
	print "--- Times Eaten ------------------------------------------------------"
	get_value = (lambda p: p.times_eaten)
	graph(people, get_value,
	              (lambda a, b: get_value(b) - get_value(a)))
	
	print
	print "--- Times Cooked/Times Eaten -----------------------------------------"
	get_value = (lambda p: round(float(p.times_cooked) / float(p.times_eaten), 4))
	graph(people, get_value,
	              (lambda a, b: int(get_value(b)*1000) - int(get_value(a)*1000)))
	
	print
	print "--- Average Times Between Cooking ------------------------------------"
	get_value = (lambda p: round(float(sum(p.times_between_cooking)) /
	                             float(len(p.times_between_cooking)), 4))
	graph(people, get_value,
	              (lambda a, b: int(get_value(b)*1000) - int(get_value(a)*1000)))
	
	print
	print "--- Min Times Between Cooking ----------------------------------------"
	get_value = (lambda p: min(p.times_between_cooking))
	graph(people, get_value,
	              (lambda a, b: get_value(b) - get_value(a)))
	
	print
	print "--- Max Times Between Cooking ----------------------------------------"
	get_value = (lambda p: max(p.times_between_cooking))
	graph(people, get_value,
	              (lambda a, b: get_value(b) - get_value(a)))



def jonnys_algorithm(_people, days):
	for day in range(days):
		people = _people[:]
		# Pick the person who cooked the longest ago
		while len(people) > 0:
			cook = min(people, key = (lambda p: p.last_cooked))
			if cook.can_cook_on_day(day):
				yield day, cook
				break
			else:
				people.remove(cook)
				continue
		
		if len(people) == 0:
			yield day, None



if __name__ == "__main__":
	main(jonnys_algorithm, 300)

