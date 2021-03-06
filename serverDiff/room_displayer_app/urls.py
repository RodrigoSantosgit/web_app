
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('departments', views.departments, name='departs'),
    path('departments_book', views.departments_book, name='departs-book'),
    path('departments_book/<int:dep_id>/', views.depart_book_rooms, name='depart-book'),
    path('departments_book/<int:dep_id>/rooms', views.depart_book_rooms, name='depart-book-rooms'),
    path('departments_book/<int:dep_id>/rooms/<int:room_id>', views.room_book_timetable, name='book-room-timetable'),

    path('method/', views.method, name='method'),
    path('book/', views.book, name='book'),
    path('departamentos/salas/<int:dep_id>/', views.salas, name='rooms'),
    path('departamentos/salas/<int:dep_id>/<int:room_id>/', views.horario_v2, name='timetable'),
    path('departamentos/salas/<int:dep_id>/<int:room_id>/location', views.location, name='location'),
    path('departamentos/soonAvailable/<int:dep_id>/<int:tD>', views.salasSoon, name='soonAvailable'),
]
