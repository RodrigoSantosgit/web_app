from django.contrib import admin

from .models import Building, Room, Event, EventType


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
	list_display = ('id', 'name','building_id')
	list_filter = ('building_id',)
	


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')
	list_filter= ('building_id','room_id')

@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')




