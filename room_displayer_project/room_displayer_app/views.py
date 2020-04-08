from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Building, Room, Event, EventType
from django.http import Http404


# Create your views here.
def index(request):
    context = {
	}
    return render(request, 'index.html', context=context)

def departments(request):
    context = {
	}
    return render(request, 'departamentos.html', context=context)

def departments_book(request):
    context = {
	}
    return render(request, 'departamentos_reserva.html', context=context)


def department_r_timetable(request, dep_id):
    context = {
	}
    return render(request, 'horario.html', context)

def department_detail(request, dep_id):
    depart = get_object_or_404(Building, id=dep_id)

    rooms = get_list_or_404(Room, building_id=dep_id)

    context = {'depart':depart, 'rooms':rooms}
    return render(request, 'depart_salas.html', context)

def room_event(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    events = get_list_or_404(Event, room_id=room_id)

    context = {'room':room, 'events':events}
    return render(request, 'sala_event.html', context)


def book(request):
    context = {
	}
    return render(request, 'departamentos.html', context=context)

def rooms(request):
    context = {
	}
    return render(request, 'salas.html', context=context)

def timetable(request):
    context = {
	}
    return render(request, 'horario.html', context=context)
