from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Building, Room, Event, EventType
from django.http import Http404
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import mysql.connector
import cv2
import numpy
import requests
import urllib
import base64

# Create your views here.
mydb = mysql.connector.connect(host="localhost", user="room_displayer",passwd="Password!23", database="room_displayer", charset='utf8mb4')
mycursor=mydb.cursor()
mycursor.execute('SET NAMES utf8;') 
mycursor.execute('SET CHARACTER SET utf8mb4;') 


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

    slQ = "SELECT * FROM Room WHERE id = %(id)s"
    mycursor.execute(slQ, { 'id': room_id })

    room_name = mycursor.fetchall()[0][1]

    context = {
	    'events' : get_events,
	    'dep_id' : dep_id,
	    'room_id': room_id,
	    'room_name' : room_name,
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
            fu = freeUntil(r[0], time)
            if int(r[1].split('.')[1]) == 1:
                salas['rooms1'] = salas['rooms1'] + [list(r) + [fu]]
            elif int(r[1].split('.')[1]) == 2:
                salas['rooms2'] = salas['rooms2'] + [list(r) + [fu]]
            elif int(r[1].split('.')[1]) == 3:
                salas['rooms3'] = salas['rooms3'] + [list(r) + [fu]]          

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

def location(request, dep_id, room_id):

    slQ = "SELECT * FROM Room WHERE id = %(id)s"
    mycursor.execute(slQ, { 'id': room_id })

    room = mycursor.fetchall()
    sala_name = room[0][1]

    x = requests.get('http://websig.ua.pt/arcgis/rest/services/ed4/electronica/MapServer/find?searchText=' + sala_name + '&contains=true&searchFields=Porta&sr=&layers=14&layerDefs=&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&dynamicLayers=&returnZ=false&returnM=false&gdbVersion=&f=pjson', stream=True)
    x_data = x.json()
    allRings = x_data['results'][0]['geometry']['rings'][0]

    rings = ProcessaListaPontos(allRings)

    x2 = requests.get('http://websig.ua.pt/ArcGIS/rest/services/ed4/electronica/MapServer/export?bbox=0&bboxSR=102161&layers=14&layerdefs=&size=960,640&imageSR=102161&format=png24&transparent=true&time=&layerTimeOptions=&f=json', stream=True)
    js = x2.json()
    mapa = js['href']
    xmin = js['extent']['xmin']
    xmax = js['extent']['xmax']
    ymin = js['extent']['ymin']
    ymax = js['extent']['ymax']
    imgW = js['width']
    imgH = js['height']

    proRings = ListaPontos(rings, xmin, xmax, ymin, ymax, imgW, imgH)

    resp = urllib.request.urlopen(mapa)
    imgn = numpy.asarray(bytearray(resp.read()), dtype = "uint8")
    img = cv2.imdecode(imgn, cv2.IMREAD_COLOR)
    img = cv2.flip(img, 0)

    prevRing = proRings[0]

    for nextring in proRings:
        cv2.line(img, (int(prevRing[0]), int(prevRing[1])), (int(nextring[0]), int(nextring[1])), (0,0,255), 2)
        prevRing = nextring

    img = cv2.flip(img, 0)

    nothing, img_str = cv2.imencode('.png', img)
    img_base64 = base64.b64encode(img_str)

    cv2.destroyAllWindows()
    del img
    del resp
    del imgn
    del img_str
	
    context = {
        'room_name': sala_name,
        'img': img_base64,
    }
	
    return render(request, 'localizacao.html', context = context)

######################################################################################

def salasSoon(request, dep_id, tD = 15):

    time = datetime.now()
    timetD = datetime.now() + timedelta(minutes=tD)
    salas = {'rooms1' : [], 'rooms2' : [], 'rooms3' : []}

    mycursor.execute("SELECT * FROM Room WHERE building_id = 4")

    myresult = mycursor.fetchall()

    salas = {'soonAvailable' : [], 'tD' : tD}

    for r in myresult:
        if not check_room_event(r[0], time):
            if check_room_event(r[0], timetD):
                salas['soonAvailable'] = salas['soonAvailable'] + [r]

    return render(request, 'salas_soon.html', salas)

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
                if (int(sd.strftime("%H")) == hora) and (int(sd.strftime("%M")) <= int(time.strftime("%M"))):
                    if int(ed.strftime("%H")) > hora:
                        return False
                elif int(ed.strftime("%H")) > hora:
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

    name = 'Reserva'

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

######################################################################################

def freeUntil(rid, time):

    slQ = "SELECT * FROM Event WHERE room_id = %(id)s"
    mycursor.execute(slQ, { 'id': rid })

    events = mycursor.fetchall()
    
    hora = int(time.strftime("%H")) + 1
    soon = [20, 0]
    if len(events) == 0:
        return "20:00"

    for e in events:
        sd = e[2]
        ed = e[3]
        if (int(sd.strftime("%d")) == int(time.strftime("%d"))) and (int(sd.strftime("%m")) == int(time.strftime("%m"))) and (int(sd.strftime("%Y")) == int(time.strftime("%Y"))):
            if int(sd.strftime("%H")) > hora:
                if int(sd.strftime("%H")) < soon[0]:
                    soon[0] = int(sd.strftime("%H"))
                    soon[1] = int(sd.strftime("%M"))
                elif int(sd.strftime("%H")) == soon[0]:
                    if int(sd.strftime("%M")) < soon[1]:
                        soon[1] = int(sd.strftime("%M"))

    if soon[1] == 0:
        return str(soon[0]) + ":" + str(soon[1]) + "0"
    else:
        return str(soon[0]) + ":" + str(soon[1])
		
#########################################################################################
		
def ListaPontos(lista_pontosf, xmin, xmax, ymin, ymax, imgW, imgH):
    res_pontos = []
    c1 = (xmax - xmin) / imgW
    c2 = (ymax - ymin) / imgH
    
    for lf in lista_pontosf:
        x = int((lf[0] - xmin) / c1)
        y = int((lf[1] - ymin) / c2)
        res_pontos += [[x,y]]

    return res_pontos;

#########################################################################################

def ProcessaListaPontos(pontos_raw):
    res1 = []
    for pontos_raw2 in pontos_raw:
        res1 += [[float(pontos_raw2[0]), float(pontos_raw2[1])]]
        
    return res1;

##########################################################################################
