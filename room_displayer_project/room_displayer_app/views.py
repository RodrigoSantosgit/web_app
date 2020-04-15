from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Building, Room, Event, EventType
from django.http import Http404
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt

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
    get_events = get_list_or_404(Event, room_id=room_id)

    context = {
	    'events' : get_events,
	    'dep_id' : dep_id,
	    'room_id': room_id,
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
@csrf_exempt
def book(request):
    dep_id = Building.objects.get(id=request.POST['dep_id'])
    room_id =Room.objects.get(id=request.POST['room_id'])
    start= request.POST['start']
    end=request.POST['end']

    context = {'dep' : dep_id, 'sala' : room_id, 'start' : start.replace('T', ' '), 'end':end.replace('T', ' ')}
    return render(request, 'reserva.html', context)

######################################################################################
def salas(request, dep_id):

    rooms = get_list_or_404(Room, building_id=dep_id)

    time = datetime.now()
    salas = {'rooms' : []}

    for r in rooms:
        if check_room_event(r.id, time):
            r.name = r.name.upper()
            salas['rooms'] = salas['rooms'] + [r]          

    return render(request, 'salas.html', salas)

######################################################################################
def horario_v2(request, dep_id, room_id):
    sala_name = get_object_or_404(Room, id=room_id).name
    get_events = get_list_or_404(Event, room_id=room_id)
    room_name = Room.objects.get(id=room_id).name
    context = {
	    'events' : get_events,
            'dep_id': dep_id,
            'room_id': room_id,
            'room_name': room_name,
	}
    return render(request, 'horario_v2.html', context=context)

######################################################################################

def horario(request, dep_id, room_id):

    sala_name = get_object_or_404(Room, id=room_id).name.upper()

    context = {'name' : sala_name, 
        'seg9': '', 'seg10': '', 'seg11': '','seg12': '', 'seg13': '','seg14': '','seg15': '','seg16': '','seg17': '','seg18': '', 'seg19': '',
        'terca9': '', 'terca10': '', 'terca11': '','terca12': '', 'terca13': '','terca14': '','terca15': '','terca16': '','terca17': '','terca18': '', 'terca19': '',
        'quarta9': '', 'quarta10': '', 'quarta11': '','quarta12': '', 'quarta13': '','quarta14': '','quarta15': '','quarta16': '','quarta17': '','quarta18': '', 'quarta19': '',
        'quinta9': '', 'quinta10': '', 'quinta11': '','quinta12': '', 'quinta13': '','quinta14': '','quinta15': '','quinta16': '','quinta17': '','quinta18': '', 'quinta19': '',
        'sexta9': '', 'sexta10': '', 'sexta11': '','sexta12': '', 'sexta13': '','sexta14': '','sexta15': '','sexta16': '','sexta17': '','sexta18': '', 'sexta19': ''}

    get_events = get_list_or_404(Event, room_id=room_id)
    
    for e in get_events:
        sd = e.Start_date
        ed = e.End_date
        if int(sd.strftime("%w")) == 1:
            fitMonday(context,sd,ed,e)
        elif int(sd.strftime("%w")) == 2:
            fitTues(context,sd,ed,e)
        elif int(sd.strftime("%w")) == 3:
            fitWed(context,sd,ed,e)
        elif int(sd.strftime("%w")) == 4:
            fitThurs(context,sd,ed,e)
        elif int(sd.strftime("%w")) == 5:
            fitFrid(context,sd,ed,e)

    return render(request, 'horario.html', context=context)

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

######################################################################################

def fitMonday(context,sd,ed,e):

    if int(sd.strftime("%H")) == 9:
        context['seg9'] += e.name

    if int(sd.strftime("%H")) == 10:
        context['seg10'] += e.name
    elif int(sd.strftime("%H")) < 10: 
        if int(ed.strftime("%H")) > 10:
            context['seg10'] += e.name
        elif int(ed.strftime("%H")) == 10 and int(ed.strftime("%M")) > 0:
            context['seg10'] += e.name

    if int(sd.strftime("%H")) == 11:
        context['seg11'] += e.name
    elif int(sd.strftime("%H")) < 11: 
        if int(ed.strftime("%H")) > 11:
            context['seg11'] += e.name
        elif int(ed.strftime("%H")) == 11 and int(ed.strftime("%M")) > 0:
            context['seg11'] += e.name

    if int(sd.strftime("%H")) == 12:
        context['seg12'] += e.name
    elif int(sd.strftime("%H")) < 12: 
        if int(ed.strftime("%H")) > 12:
            context['seg12'] += e.name
        elif int(ed.strftime("%H")) == 12 and int(ed.strftime("%M")) > 0:
            context['seg12'] += e.name

    if int(sd.strftime("%H")) == 13:
        context['seg13'] += e.name
    elif int(sd.strftime("%H")) < 13: 
        if int(ed.strftime("%H")) > 13:
            context['seg13'] += e.name
        elif int(ed.strftime("%H")) == 13 and int(ed.strftime("%M")) > 0:
            context['seg13'] += e.name

    if int(sd.strftime("%H")) == 14:
        context['seg14'] += e.name
    elif int(sd.strftime("%H")) < 14: 
        if int(ed.strftime("%H")) > 14:
            context['seg14'] += e.name
        elif int(ed.strftime("%H")) == 14 and int(ed.strftime("%M")) > 0:
            context['seg14'] += e.name

    if int(sd.strftime("%H")) == 15:
        context['seg15'] += e.name
    elif int(sd.strftime("%H")) < 15: 
        if int(ed.strftime("%H")) > 15:
            context['seg15'] += e.name
        elif int(ed.strftime("%H")) == 15 and int(ed.strftime("%M")) > 0:
            context['seg15'] += e.name

    if int(sd.strftime("%H")) == 16:
        context['seg16'] += e.name
    elif int(sd.strftime("%H")) < 16: 
        if int(ed.strftime("%H")) > 16:
            context['seg16'] += e.name
        elif int(ed.strftime("%H")) == 16 and int(ed.strftime("%M")) > 0:
            context['seg16'] += e.name

    if int(sd.strftime("%H")) == 17:
        context['seg17'] += e.name
    elif int(sd.strftime("%H")) < 17: 
        if int(ed.strftime("%H")) > 17:
            context['seg17'] += e.name
        elif int(ed.strftime("%H")) == 17 and int(ed.strftime("%M")) > 0:
            context['seg17'] += e.name

    if int(sd.strftime("%H")) == 18:
        context['seg18'] += e.name
    elif int(sd.strftime("%H")) < 18: 
        if int(ed.strftime("%H")) > 18:
            context['seg18'] += e.name
        elif int(ed.strftime("%H")) == 18 and int(ed.strftime("%M")) > 0:
            context['seg18'] += e.name

    if int(sd.strftime("%H")) == 19:
        context['seg19'] += e.name
    elif int(sd.strftime("%H")) < 19: 
        if int(ed.strftime("%H")) > 19:
            context['seg19'] += e.name
        elif int(ed.strftime("%H")) == 19 and int(ed.strftime("%M")) > 0:
            context['seg19'] += e.name

######################################################################################

def fitTues(context,sd,ed,e):
    
    if int(sd.strftime("%H")) == 9:
        context['terca9'] += e.name

    if int(sd.strftime("%H")) == 10:
        context['terca10'] += e.name
    elif int(sd.strftime("%H")) < 10: 
        if int(ed.strftime("%H")) > 10:
            context['terca10'] += e.name
        elif int(ed.strftime("%H")) == 10 and int(ed.strftime("%M")) > 0:
            context['terca10'] += e.name

    if int(sd.strftime("%H")) == 11:
        context['terca11'] += e.name
    elif int(sd.strftime("%H")) < 11: 
        if int(ed.strftime("%H")) > 11:
            context['terca11'] += e.name
        elif int(ed.strftime("%H")) == 11 and int(ed.strftime("%M")) > 0:
            context['terca11'] += e.name

    if int(sd.strftime("%H")) == 12:
        context['terca12'] += e.name
    elif int(sd.strftime("%H")) < 12: 
        if int(ed.strftime("%H")) > 12:
            context['terca12'] += e.name
        elif int(ed.strftime("%H")) == 12 and int(ed.strftime("%M")) > 0:
            context['terca12'] += e.name

    if int(sd.strftime("%H")) == 13:
        context['terca13'] += e.name
    elif int(sd.strftime("%H")) < 13: 
        if int(ed.strftime("%H")) > 13:
            context['terca13'] += e.name
        elif int(ed.strftime("%H")) == 13 and int(ed.strftime("%M")) > 0:
            context['terca13'] += e.name

    if int(sd.strftime("%H")) == 14:
        context['terca14'] += e.name
    elif int(sd.strftime("%H")) < 14: 
        if int(ed.strftime("%H")) > 14:
            context['terca14'] += e.name
        elif int(ed.strftime("%H")) == 14 and int(ed.strftime("%M")) > 0:
            context['terca14'] += e.name

    if int(sd.strftime("%H")) == 15:
        context['terca15'] += e.name
    elif int(sd.strftime("%H")) < 15: 
        if int(ed.strftime("%H")) > 15:
            context['terca15'] += e.name
        elif int(ed.strftime("%H")) == 15 and int(ed.strftime("%M")) > 0:
            context['terca15'] += e.name

    if int(sd.strftime("%H")) == 16:
        context['terca16'] += e.name
    elif int(sd.strftime("%H")) < 16: 
        if int(ed.strftime("%H")) > 16:
            context['terca16'] += e.name
        elif int(ed.strftime("%H")) == 16 and int(ed.strftime("%M")) > 0:
            context['terca16'] += e.name

    if int(sd.strftime("%H")) == 17:
        context['terca17'] += e.name
    elif int(sd.strftime("%H")) < 17: 
        if int(ed.strftime("%H")) > 17:
            context['terca17'] += e.name
        elif int(ed.strftime("%H")) == 17 and int(ed.strftime("%M")) > 0:
            context['terca17'] += e.name

    if int(sd.strftime("%H")) == 18:
        context['terca18'] += e.name
    elif int(sd.strftime("%H")) < 18: 
        if int(ed.strftime("%H")) > 18:
            context['terca18'] += e.name
        elif int(ed.strftime("%H")) == 18 and int(ed.strftime("%M")) > 0:
            context['terca18'] += e.name

    if int(sd.strftime("%H")) == 19:
        context['terca19'] += e.name
    elif int(sd.strftime("%H")) < 19: 
        if int(ed.strftime("%H")) > 19:
            context['terca19'] += e.name
        elif int(ed.strftime("%H")) == 19 and int(ed.strftime("%M")) > 0:
            context['terca19'] += e.name

######################################################################################

def fitWed(context,sd,ed,e):
    
    if int(sd.strftime("%H")) == 9:
        context['quarta9'] += e.name

    if int(sd.strftime("%H")) == 10:
        context['quarta10'] += e.name
    elif int(sd.strftime("%H")) < 10: 
        if int(ed.strftime("%H")) > 10:
            context['quarta10'] += e.name
        elif int(ed.strftime("%H")) == 10 and int(ed.strftime("%M")) > 0:
            context['quarta10'] += e.name

    if int(sd.strftime("%H")) == 11:
        context['quarta11'] += e.name
    elif int(sd.strftime("%H")) < 11: 
        if int(ed.strftime("%H")) > 11:
            context['quarta11'] += e.name
        elif int(ed.strftime("%H")) == 11 and int(ed.strftime("%M")) > 0:
            context['quarta11'] += e.name

    if int(sd.strftime("%H")) == 12:
        context['quarta12'] += e.name
    elif int(sd.strftime("%H")) < 12: 
        if int(ed.strftime("%H")) > 12:
            context['quarta12'] += e.name
        elif int(ed.strftime("%H")) == 12 and int(ed.strftime("%M")) > 0:
            context['quarta12'] += e.name

    if int(sd.strftime("%H")) == 13:
        context['quarta13'] += e.name
    elif int(sd.strftime("%H")) < 13: 
        if int(ed.strftime("%H")) > 13:
            context['quarta13'] += e.name
        elif int(ed.strftime("%H")) == 13 and int(ed.strftime("%M")) > 0:
            context['quarta13'] += e.name

    if int(sd.strftime("%H")) == 14:
        context['quarta14'] += e.name
    elif int(sd.strftime("%H")) < 14: 
        if int(ed.strftime("%H")) > 14:
            context['quarta14'] += e.name
        elif int(ed.strftime("%H")) == 14 and int(ed.strftime("%M")) > 0:
            context['quarta14'] += e.name

    if int(sd.strftime("%H")) == 15:
        context['quarta15'] += e.name
    elif int(sd.strftime("%H")) < 15: 
        if int(ed.strftime("%H")) > 15:
            context['quarta15'] += e.name
        elif int(ed.strftime("%H")) == 15 and int(ed.strftime("%M")) > 0:
            context['quarta15'] += e.name

    if int(sd.strftime("%H")) == 16:
        context['quarta16'] += e.name
    elif int(sd.strftime("%H")) < 16: 
        if int(ed.strftime("%H")) > 16:
            context['quarta16'] += e.name
        elif int(ed.strftime("%H")) == 16 and int(ed.strftime("%M")) > 0:
            context['quarta16'] += e.name

    if int(sd.strftime("%H")) == 17:
        context['quarta17'] += e.name
    elif int(sd.strftime("%H")) < 17: 
        if int(ed.strftime("%H")) > 17:
            context['quarta17'] += e.name
        elif int(ed.strftime("%H")) == 17 and int(ed.strftime("%M")) > 0:
            context['quarta17'] += e.name

    if int(sd.strftime("%H")) == 18:
        context['quarta18'] += e.name
    elif int(sd.strftime("%H")) < 18: 
        if int(ed.strftime("%H")) > 18:
            context['quarta18'] += e.name
        elif int(ed.strftime("%H")) == 18 and int(ed.strftime("%M")) > 0:
            context['quarta18'] += e.name

    if int(sd.strftime("%H")) == 19:
        context['quarta19'] += e.name
    elif int(sd.strftime("%H")) < 19: 
        if int(ed.strftime("%H")) > 19:
            context['quarta19'] += e.name
        elif int(ed.strftime("%H")) == 19 and int(ed.strftime("%M")) > 0:
            context['quarta19'] += e.name

######################################################################################

def fitThurs(context,sd,ed,e):
    
    if int(sd.strftime("%H")) == 9:
        context['quinta9'] = e.name

    if int(sd.strftime("%H")) == 10:
        context['quinta10'] = e.name
    elif int(sd.strftime("%H")) < 10: 
        if int(ed.strftime("%H")) > 10:
            context['quinta10'] = e.name
        elif int(ed.strftime("%H")) == 10 and int(ed.strftime("%M")) > 0:
            context['quinta10'] = e.name

    if int(sd.strftime("%H")) == 11:
        context['quinta11'] = e.name
    elif int(sd.strftime("%H")) < 11: 
        if int(ed.strftime("%H")) > 11:
            context['quinta11'] = e.name
        elif int(ed.strftime("%H")) == 11 and int(ed.strftime("%M")) > 0:
            context['quinta11'] = e.name

    if int(sd.strftime("%H")) == 12:
        context['quinta12'] = e.name
    elif int(sd.strftime("%H")) < 12: 
        if int(ed.strftime("%H")) > 12:
            context['quinta12'] = e.name
        elif int(ed.strftime("%H")) == 12 and int(ed.strftime("%M")) > 0:
            context['quinta12'] = e.name

    if int(sd.strftime("%H")) == 13:
        context['quinta13'] = e.name
    elif int(sd.strftime("%H")) < 13: 
        if int(ed.strftime("%H")) > 13:
            context['quinta13'] = e.name
        elif int(ed.strftime("%H")) == 13 and int(ed.strftime("%M")) > 0:
            context['quinta13'] = e.name

    if int(sd.strftime("%H")) == 14:
        context['quinta14'] = e.name
    elif int(sd.strftime("%H")) < 14: 
        if int(ed.strftime("%H")) > 14:
            context['quinta14'] = e.name
        elif int(ed.strftime("%H")) == 14 and int(ed.strftime("%M")) > 0:
            context['quinta14'] = e.name

    if int(sd.strftime("%H")) == 15:
        context['quinta15'] = e.name
    elif int(sd.strftime("%H")) < 15: 
        if int(ed.strftime("%H")) > 15:
            context['quinta15'] = e.name
        elif int(ed.strftime("%H")) == 15 and int(ed.strftime("%M")) > 0:
            context['quinta15'] = e.name

    if int(sd.strftime("%H")) == 16:
        context['quinta16'] = e.name
    elif int(sd.strftime("%H")) < 16: 
        if int(ed.strftime("%H")) > 16:
            context['quinta16'] = e.name
        elif int(ed.strftime("%H")) == 16 and int(ed.strftime("%M")) > 0:
            context['quinta16'] = e.name

    if int(sd.strftime("%H")) == 17:
        context['quinta17'] = e.name
    elif int(sd.strftime("%H")) < 17: 
        if int(ed.strftime("%H")) > 17:
            context['quinta17'] = e.name
        elif int(ed.strftime("%H")) == 17 and int(ed.strftime("%M")) > 0:
            context['quinta17'] = e.name

    if int(sd.strftime("%H")) == 18:
        context['quinta18'] = e.name
    elif int(sd.strftime("%H")) < 18: 
        if int(ed.strftime("%H")) > 18:
            context['quinta18'] = e.name
        elif int(ed.strftime("%H")) == 18 and int(ed.strftime("%M")) > 0:
            context['quinta18'] = e.name

    if int(sd.strftime("%H")) == 19:
        context['quinta19'] = e.name
    elif int(sd.strftime("%H")) < 19: 
        if int(ed.strftime("%H")) > 19:
            context['quinta19'] = e.name
        elif int(ed.strftime("%H")) == 19 and int(ed.strftime("%M")) > 0:
            context['quinta19'] = e.name

######################################################################################

def fitFrid(context,sd,ed,e):
    
    if int(sd.strftime("%H")) == 9:
        context['sexta9'] = e.name

    if int(sd.strftime("%H")) == 10:
        context['sexta10'] = e.name
    elif int(sd.strftime("%H")) < 10: 
        if int(ed.strftime("%H")) > 10:
            context['sexta10'] = e.name
        elif int(ed.strftime("%H")) == 10 and int(ed.strftime("%M")) > 0:
            context['sexta10'] = e.name

    if int(sd.strftime("%H")) == 11:
        context['sexta11'] = e.name
    elif int(sd.strftime("%H")) < 11: 
        if int(ed.strftime("%H")) > 11:
            context['sexta11'] = e.name
        elif int(ed.strftime("%H")) == 11 and int(ed.strftime("%M")) > 0:
            context['sexta11'] = e.name

    if int(sd.strftime("%H")) == 12:
        context['sexta12'] = e.name
    elif int(sd.strftime("%H")) < 12: 
        if int(ed.strftime("%H")) > 12:
            context['sexta12'] = e.name
        elif int(ed.strftime("%H")) == 12 and int(ed.strftime("%M")) > 0:
            context['sexta12'] = e.name

    if int(sd.strftime("%H")) == 13:
        context['sexta13'] = e.name
    elif int(sd.strftime("%H")) < 13: 
        if int(ed.strftime("%H")) > 13:
            context['sexta13'] = e.name
        elif int(ed.strftime("%H")) == 13 and int(ed.strftime("%M")) > 0:
            context['sexta13'] = e.name

    if int(sd.strftime("%H")) == 14:
        context['sexta14'] = e.name
    elif int(sd.strftime("%H")) < 14: 
        if int(ed.strftime("%H")) > 14:
            context['sexta14'] = e.name
        elif int(ed.strftime("%H")) == 14 and int(ed.strftime("%M")) > 0:
            context['sexta14'] = e.name

    if int(sd.strftime("%H")) == 15:
        context['sexta15'] = e.name
    elif int(sd.strftime("%H")) < 15: 
        if int(ed.strftime("%H")) > 15:
            context['sexta15'] = e.name
        elif int(ed.strftime("%H")) == 15 and int(ed.strftime("%M")) > 0:
            context['sexta15'] = e.name

    if int(sd.strftime("%H")) == 16:
        context['sexta16'] = e.name
    elif int(sd.strftime("%H")) < 16: 
        if int(ed.strftime("%H")) > 16:
            context['sexta16'] = e.name
        elif int(ed.strftime("%H")) == 16 and int(ed.strftime("%M")) > 0:
            context['sexta16'] = e.name

    if int(sd.strftime("%H")) == 17:
        context['sexta17'] = e.name
    elif int(sd.strftime("%H")) < 17: 
        if int(ed.strftime("%H")) > 17:
            context['sexta17'] = e.name
        elif int(ed.strftime("%H")) == 17 and int(ed.strftime("%M")) > 0:
            context['sexta17'] = e.name

    if int(sd.strftime("%H")) == 18:
        context['sexta18'] = e.name
    elif int(sd.strftime("%H")) < 18: 
        if int(ed.strftime("%H")) > 18:
            context['sexta18'] = e.name
        elif int(ed.strftime("%H")) == 18 and int(ed.strftime("%M")) > 0:
            context['sexta18'] = e.name

    if int(sd.strftime("%H")) == 19:
        context['sexta19'] = e.name
    elif int(sd.strftime("%H")) < 19: 
        if int(ed.strftime("%H")) > 19:
            context['sexta19'] = e.name
        elif int(ed.strftime("%H")) == 19 and int(ed.strftime("%M")) > 0:
            context['sexta19'] = e.name

