from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Building, Room, Event, EventType
from django.http import Http404
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy
import requests
import urllib
import base64
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

    context = {'depart':depart, 'rooms1': [], 'rooms2': [], 'rooms3': []}
    for r in rooms:
        r.name = r.name.upper()
        if not (r.name[0].isdigit()):
            context['rooms1'] = context['rooms1'] + [r]
        elif int(r.name.split('.')[1]) == 1:
            context['rooms1'] = context['rooms1'] + [r]
        elif int(r.name.split('.')[1]) == 2:
            context['rooms2'] = context['rooms2'] + [r]
        elif int(r.name.split('.')[1]) == 3:
            context['rooms3'] = context['rooms3'] + [r]


    
    return render(request, 'departamento_reserva_salas.html', context)

######################################################################################

def room_book_timetable(request, dep_id, room_id):
    get_events = get_list_or_404(Event, room_id=room_id)
    room_name = Room.objects.get(id=room_id).name.upper()

    context = {
	    'events' : get_events,
	    'dep_id' : dep_id,
	    'room_id': room_id,
        'room_name': room_name,
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

@csrf_exempt
def book(request):
    dep_id = Building.objects.get(id=request.POST['dep_id'])
    room_id =Room.objects.get(id=request.POST['room_id'])
    start= request.POST['start']
    end=request.POST['end']

    context = {'dep' : dep_id, 'sala' : room_id, 
        'start' : (start[0:4] + '/' + start[5:7] + '/' + start[8:10] + ' - ' + start[11:13] + ':' + start[14:16]), 
        'end' : (end[0:4] + '/' + end[5:7] + '/' + end[8:10] + ' - ' + end[11:13] + ':' + end[14:16])}
    return render(request, 'reserva.html', context)

######################################################################################

def salas(request, dep_id, tD=15):

    rooms = get_list_or_404(Room, building_id=dep_id)

    time = datetime.now()
    timetD = datetime.now() + timedelta(minutes=tD)

    salas = {'rooms1' : [], 'rooms2' : [], 'rooms3' : [], 'soonAvailable' : [], 'tD' : tD}

    for r in rooms:
        if check_room_event(r.id, time):
            r.name = r.name.upper()
            fu = freeUntil(r.id, time)
            if not (r.name[0].isdigit()):
                salas['rooms1'] = salas['rooms1'] + [(r, fu)]
            elif int(r.name.split('.')[1]) == 1:
                salas['rooms1'] = salas['rooms1'] + [(r, fu)]
            elif int(r.name.split('.')[1]) == 2:
                salas['rooms2'] = salas['rooms2'] + [(r, fu)]
            elif int(r.name.split('.')[1]) == 3:
                salas['rooms3'] = salas['rooms3'] + [(r, fu)]
        elif check_room_event(r.id, timetD):
            r.name = r.name.upper()
            salas['soonAvailable'] = salas['soonAvailable'] + [r]        

    return render(request, 'salas.html', salas)

######################################################################################

def salasSoon(request, dep_id, tD=30):

    rooms = get_list_or_404(Room, building_id=dep_id)

    time = datetime.now()
    timetD = datetime.now() + timedelta(minutes=tD)

    salas = {'soonAvailable' : [], 'tD' : tD}

    for r in rooms:
        if not check_room_event(r.id, time):
            if check_room_event(r.id, timetD):
                nextE = check_room_event(r.id, time, 1)
                r.name = r.name.upper()
                salas['soonAvailable'] = salas['soonAvailable'] + [(r, datetime(year=int(nextE.strftime("%Y")),month=int(nextE.strftime("%m")),day = int(nextE.strftime("%d")), hour= int(nextE.strftime("%H")), minute= int(nextE.strftime("%M")), second= 0)-
                    datetime(year=int(time.strftime("%Y")),month=int(time.strftime("%m")),day = int(time.strftime("%d")), hour= int(time.strftime("%H")) + 1, minute= int(time.strftime("%M")), second = int(time.strftime("%S"))))]        

    return render(request, 'salas_soon.html', salas)

######################################################################################

def horario_v2(request, dep_id, room_id):
    sala_name = get_object_or_404(Room, id=room_id).name
    get_events = get_list_or_404(Event, room_id=room_id)
    room_name = Room.objects.get(id=room_id).name.upper()
    context = {
	    'events' : get_events,
            'dep_id': dep_id,
            'room_id': room_id,
            'room_name': room_name,
	}
    return render(request, 'horario_v2.html', context=context)

######################################################################################

def location(request, dep_id, room_id):

    sala_name = get_object_or_404(Room, id=room_id).name.upper()

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
    img = numpy.asarray(bytearray(resp.read()), dtype = "uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    img = cv2.flip(img, 0)

    prevRing = proRings[0]

    for nextring in proRings:
        cv2.line(img, (int(prevRing[0]), int(prevRing[1])), (int(nextring[0]), int(nextring[1])), (0,0,255), 2)
        prevRing = nextring

    img = cv2.flip(img, 0)

    nothing, img_str = cv2.imencode('.png', img)
    img_base64 = base64.b64encode(img_str)
    print(img_base64[2:-1])
    context = {
        'room_name': sala_name,
        'img': img_base64,
    }

    return render(request, 'localizacao.html', context = context)

######################################################################################
######################################################################################

# FUNCOES AUXILIARES 

######################################################################################

def check_room_event(rid, time, soon=0):

    events = list(Event.objects.filter(room_id=rid))
    
    hora = int(time.strftime("%H")) + 1

    if len(events) == 0:
        return True

    for e in events:
        sd = e.Start_date
        ed = e.End_date
        if (int(sd.strftime("%d")) == int(time.strftime("%d"))) and (int(sd.strftime("%m")) == int(time.strftime("%m"))) and (int(sd.strftime("%Y")) == int(time.strftime("%Y"))):
            if int(sd.strftime("%H")) <= hora:
                if int(ed.strftime("%H")) > hora:
                    if not soon:
                        return False
                    else :
                        return ed
                elif int(ed.strftime("%H")) == hora:
                    if int(ed.strftime("%M")) > int(time.strftime("%M")):
                        if not soon:
                            return False
                        else:
                            return ed


    return True

######################################################################################

def freeUntil(rid, time):

    events = list(Event.objects.filter(room_id=rid))
    soon = [20, 0]
    hora = int(time.strftime("%H")) + 1


    if len(events) == 0:
        return "20:00"

    for e in events:
        sd = e.Start_date
        ed = e.End_date
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

######################################################################################

##########################################################################################

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