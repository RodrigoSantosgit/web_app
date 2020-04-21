from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Building, Room, Event, EventType
from django.http import Http404
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
# Create your views here.
mydb = mysql.connector.connect(host="localhost", user="room_displayer",passwd="Password!23", database="room_displayer")
mycursor=mydb.cursor()

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
    #depart = get_object_or_404(Building, id=dep_id)

    #rooms = get_list_or_404(Room, building_id=dep_id)
    depart = (4,'DETI')
    context = {'depart':depart, 'rooms1': [], 'rooms2': [], 'rooms3': []}
    mycursor.execute("SELECT * FROM Room WHERE building_id = 4")

    myresult = mycursor.fetchall()
    for r in myresult:
    #    r.name = r.name.upper()
    #    if not (r.name[0].isdigit()):
    #        context['rooms1'] = context['rooms1'] + [r]
    #    elif int(r.name.split('.')[1]) == 1:
    #        context['rooms1'] = context['rooms1'] + [r]
    #    elif int(r.name.split('.')[1]) == 2:
    #        context['rooms2'] = context['rooms2'] + [r]
    #    elif int(r.name.split('.')[1]) == 3:
    #        context['rooms3'] = context['rooms3'] + [r]
            if int(r[1].split('.')[1]) == 1:
                context['rooms1'] = context['rooms1'] + [r]
            elif int(r[1].split('.')[1]) == 2:
                context['rooms2'] = context['rooms2'] + [r]
            elif int(r[1].split('.')[1]) == 3:
                context['rooms3'] = context['rooms3'] + [r] 

    
    return render(request, 'departamento_reserva_salas.html', context)

######################################################################################

def room_book_timetable(request, dep_id, room_id):
    #get_events = get_list_or_404(Event, room_id=room_id)
	
    slQ = "SELECT * FROM Event WHERE room_id = %(id)s"
    mycursor.execute(slQ, { 'id': room_id })

    get_events = mycursor.fetchall()

    context = {
	    'events' : get_events,
	    'dep_id' : dep_id,
	    'room_id': room_id,
	}
    return render(request, 'horario_book_c.html', context=context)

######################################################################################


######################################################################################

@csrf_exempt
def book(request):
    #dep_id = Building.objects.get(id=request.POST['dep_id'])
    slQ = "SELECT * FROM Building WHERE id = %(id)s"
    mycursor.execute(slQ, { 'id': request.POST.get('dep_id') })

    dep = mycursor.fetchall()

    #room_id =Room.objects.get(id=request.POST['room_id'])
    slQ = "SELECT * FROM Room WHERE id = %(id)s"
    mycursor.execute(slQ, { 'id': request.POST.get('room_id') })

    room = mycursor.fetchall()

    start= request.POST.get('start')
    end=request.POST.get('end')
    if start != None or end != None:
        context = {'dep' : dep, 'sala' : room, 
            'start' : (start[0:4] + '/' + start[5:7] + '/' + start[8:10] + ' - ' + start[11:13] + ':' + start[14:16]), 
            'end' : (end[0:4] + '/' + end[5:7] + '/' + end[8:10] + ' - ' + end[11:13] + ':' + end[14:16]),
            'sd' : start, 'ed' : end}
    else:
        context = {}
    return render(request, 'reserva.html', context)

######################################################################################

def salas(request, dep_id):

    #rooms = get_list_or_404(Room, building_id=dep_id)

    time = datetime.now()
    salas = {'rooms1' : [], 'rooms2' : [], 'rooms3' : []}
    
    mycursor.execute("SELECT * FROM Room WHERE building_id = 4")

    myresult = mycursor.fetchall()
    

    for r in myresult:
        if check_room_event(r[0], time):
    #        r.name = r.name.upper()
    #        if not (r.name[0].isdigit()):
    #            salas['rooms1'] = salas['rooms1'] + [r]
            if int(r[1].split('.')[1]) == 1:
                salas['rooms1'] = salas['rooms1'] + [r]
            elif int(r[1].split('.')[1]) == 2:
                salas['rooms2'] = salas['rooms2'] + [r]
            elif int(r[1].split('.')[1]) == 3:
                salas['rooms3'] = salas['rooms3'] + [r]          

    return render(request, 'salas.html', salas)

######################################################################################

def horario_v2(request, dep_id, room_id):
    slQ = "SELECT * FROM Room WHERE id = %(id)s"
    mycursor.execute(slQ, { 'id': room_id })

    room = mycursor.fetchall()
    #sala_name = get_object_or_404(Room, id=room_id).name
    room_name = room[0][1]
	
    slQ = "SELECT * FROM Event WHERE room_id = %(id)s"
    mycursor.execute(slQ, { 'id': room_id })

    get_events = mycursor.fetchall()
    #get_events = get_list_or_404(Event, room_id=room_id)
    #room_name = Room.objects.get(id=room_id).name.upper()
    context = {
	    'events' : get_events,
            'dep_id': dep_id,
            'room_id': room_id,
            'room_name': room_name,
	}
    return render(request, 'horario_v2.html', context=context)

######################################################################################

######################################################################################

# FUNCOES AUXILIARES 

######################################################################################

def check_room_event(rid, time):

    #events = list(Event.objects.filter(room_id=rid))
    
    slQ = "SELECT * FROM Event WHERE room_id = %(id)s"
    mycursor.execute(slQ, { 'id': rid })

    events = mycursor.fetchall()
    
    hora = int(time.strftime("%H")) + 1

    if len(events) == 0:
        return True

    #for e in events:
    #    sd = e.Start_date
    #    ed = e.End_date
    #   if (int(sd.strftime("%d")) == int(time.strftime("%d"))) and (int(sd.strftime("%m")) == int(time.strftime("%m"))) and (int(sd.strftime("%Y")) == int(time.strftime("%Y"))):
    #        if int(sd.strftime("%H")) <= hora:
    #            if int(ed.strftime("%H")) > hora:
    #                return False
    #            elif int(ed.strftime("%H")) == hora:
    #                if int(ed.strftime("%M")) > int(time.strftime("%M")):
    #                    return False

    for e in events:
        sd = e[2]
        ed = e[3]
        if (int(sd.strftime("%d")) == int(time.strftime("%d"))) and (int(sd.strftime("%m")) == int(time.strftime("%m"))) and (int(sd.strftime("%Y")) == int(time.strftime("%Y"))):
            if int(sd.strftime("%H")) <= hora:
                if int(ed.strftime("%H")) > hora:
                    return False
                elif int(ed.strftime("%H")) == hora:
                    if int(ed.strftime("%M")) > int(time.strftime("%M")):
                        return False

    return True

######################################################################################
@csrf_exempt
def method(request):
    dep = request.POST['dep_id']

    room = request.POST['room_id']

    sd = request.POST['start']
    ed = request.POST['end']

    type = 3

    name = 'Reserva Rodrigo'

    participants = 1
    slQ = "SELECT * FROM Event"
    mycursor.execute(slQ)

    get_events = mycursor.fetchall()
    id = get_events[-1][0] + 1 
    insert_stmt = (
        "INSERT INTO Event (id, name, Start_date, End_date, type, participants, building_id, room_id) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    )
    data = (id, name, sd, ed, type, participants, dep, room)
    mycursor.execute(insert_stmt, data)
	
    slQ = "SELECT * FROM Event WHERE room_id = %(id)s"
    mycursor.execute(slQ, { 'id': room })

    get_events = mycursor.fetchall()

    context = {
	    'events' : get_events,
	    'dep_id' : dep,
	    'room_id': room,
	}
    return render(request, 'horario_book_c.html', context=context)
