from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Building, Room, Event, EventType
from django.http import Http404
from datetime import datetime

# Create your views here.

def index(request):
    context = {
	}
    return render(request, 'index.html', context=context)

######################################################################################

def departments(request):
    context = {
	}
    return render(request, 'departamentos.html', context=context)

######################################################################################

def departments_book(request):
    context = {
	}
    return render(request, 'departamentos_reserva.html', context=context)
######################################################################################

def depart_book_rooms(request, dep_id):
    depart = get_object_or_404(Building, id=dep_id)

    rooms = get_list_or_404(Room, building_id=dep_id)

    context = {'depart':depart, 'rooms':rooms}
    return render(request, 'departamento_reserva_salas.html', context)

######################################################################################
def room_book_timetable(request, dep_id, room_id):
    events = get_list_or_404(Event, room_id=room_id)
    context = {
	    'events' : events
	}
    return render(request, 'horario_book_c.html', context=context)

######################################################################################


######################################################################################

def department_detail(request, dep_id):
    depart = get_object_or_404(Building, id=dep_id)

    rooms = get_list_or_404(Room, building_id=dep_id)

    context = {'depart':depart, 'rooms':rooms}
    return render(request, 'depart_salas.html', context)

######################################################################################

def room_event(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    events = get_list_or_404(Event, room_id=room_id)

    context = {'room':room, 'events':events}
    return render(request, 'sala_event.html', context)

######################################################################################

def book(request):
    context = {
	}
    return render(request, 'reserva.html', context=context)

######################################################################################

def salas(request, dep_id):

    rooms = get_list_or_404(Room, building_id=dep_id)

    time = datetime.now()
    salas = {'rooms' : []}

    for r in rooms:
        if check_room_event(r.id, time):
            name = str(r.name)
            salas['rooms'] = salas['rooms'] + [name.upper()]          

    return render(request, 'salas.html', salas)

######################################################################################

def timetable(request):
    context = {
	}
    return render(request, 'horario.html', context=context)

######################################################################################

def horario(request, dep_id, sala_name):

    context = {'name' : [str(sala_name)]}
    return render(request, 'horario.html', context)

######################################################################################

# FUNCOES AUXILIARES 

######################################################################################

def check_room_event(rid, time):

    events = list(Event.objects.filter(room_id=rid))
    
    hora = int(time.strftime("%H")) + 1

    if len(events) == 0:
        return True

    for e in events:
        sd = e.Start_date
        ed = e.End_date
        if int(sd.strftime("%w")) == int(time.strftime("%w")):
            if int(sd.strftime("%H")) <= hora:
                if int(ed.strftime("%H")) > hora:
                    return False
                elif int(ed.strftime("%H")) == hora:
                    if int(ed.strftime("%M")) > int(time.strftime("%M")):
                        return False


    return True
