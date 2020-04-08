from django.db import models

class Building(models.Model):
	"""Model representing department"""

	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100, help_text='Enter name of department')

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('departs-detail', args=[self.id])

class Room(models.Model):
	"""Model representing room"""
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	capacity = models.IntegerField()
	email = models.EmailField(null=True, blank=True)
	building_id = models.ForeignKey('Building', on_delete=models.SET_NULL, null=True)
	#event = models.ManyToManyField(Event, blank=True, null=True)
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('rooms-detail', args=[self.id])

	def by_depart(self, dep_id):	
		return self.building_id == dep_id
	
	

class Event(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)
	Start_date = models.DateTimeField(null=True, blank=True)
	End_date = models.DateTimeField(null=True, blank=True)
	type = models.ForeignKey('EventType', on_delete=models.SET_NULL, null=True)
	participants = models.IntegerField(null=True, blank=True)
	building_id = models.ForeignKey('Building', on_delete=models.SET_NULL, null=True)
	room_id = models.ForeignKey('Room', on_delete=models.SET_NULL, null=True)
	
	def __str__(self):
		return self.name


class EventType(models.Model):
	id = models.IntegerField(primary_key=True)
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name
