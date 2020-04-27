from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Building, Room, Event, EventType
from django.http import Http404
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
# Create your views here.
mydb = mysql.connector.connect(host="localhost", user="room_displayer",passwd="Password!23", database="room_displayer", charset='utf8', use_unicode=True)
mycursor=mydb.cursor()
mycursor.execute('SET NAMES utf8;') 
mycursor.execute('SET CHARACTER SET utf8;') 
mycursor.execute('SET character_set_connection=utf8;')

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
    
    depart = (4,'DETI')
    context = {'depart':depart, 'rooms1': [], 'rooms2': [], 'rooms3': []}
    mycursor.execute("SELECT * FROM Room WHERE building_id = 4")

    myresult = mycursor.fetchall()
    for r in myresult:
        if int(r[1].split('.')[1]) == 1:
            context['rooms1'] = context['rooms1'] + [r]
        elif int(r[1].split('.')[1]) == 2:
            context['rooms2'] = context['rooms2'] + [r]
        elif int(r[1].split('.')[1]) == 3:
            context['rooms3'] = context['rooms3'] + [r] 

    
    return render(request, 'departamento_reserva_salas.html', context)

######################################################################################

def room_book_timetable(request, dep_id, room_id):

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

    slQ = "SELECT * FROM Building WHERE id = %(id)s"
    mycursor.execute(slQ, { 'id': request.POST.get('dep_id') })

    dep = mycursor.fetchall()


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

    time = datetime.now()
    salas = {'rooms1' : [], 'rooms2' : [], 'rooms3' : []}
    
    mycursor.execute("SELECT * FROM Room WHERE building_id = 4")

    myresult = mycursor.fetchall()
    

    for r in myresult:
        if check_room_event(r[0], time):
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

    room_name = room[0][1]
	
    slQ = "SELECT * FROM Event WHERE room_id = %(id)s"
    mycursor.execute(slQ, { 'id': room_id })

    get_events = mycursor.fetchall()

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

    slQ = "SELECT * FROM Event WHERE room_id = %(id)s"
    mycursor.execute(slQ, { 'id': rid })

    events = mycursor.fetchall()
    
    hora = int(time.strftime("%H")) + 1

    if len(events) == 0:
        return True

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

    if (int(ed[8:10]) != int(sd[8:10])) or (int(ed[11:13]) - int(sd[11:13])) > 2 or ((int(ed[11:13]) - int(sd[11:13])) == 2 and (int(ed[14:16]) - int(sd[14:16]) == 30)):
        slQ = "SELECT * FROM Building WHERE id = %(id)s"
        mycursor.execute(slQ, { 'id': request.POST.get('dep_id') })

        dep = mycursor.fetchall()

        slQ = "SELECT * FROM Room WHERE id = %(id)s"
        mycursor.execute(slQ, { 'id': request.POST.get('room_id') })

        room = mycursor.fetchall()
        context = {'dep' : dep, 'sala' : room, 'start' : '', 'end' : '', 'sd' : '', 'ed' : ''}
        return render(request, 'reserva.html', context=context)

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
