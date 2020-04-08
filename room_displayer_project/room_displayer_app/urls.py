
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('departments', views.departments, name='departs'),
    path('departments_book', views.departments_book, name='departs-book'),
    path('departments_book/<int:dep_id>/', views.department_r_timetable, name='depart-book'),
    path('departaments/<int:dep_id>/', views.department_detail, name='depart-detail'),
    path('departaments/events/<int:room_id>/', views.room_event, name='room-event'),
    path('book', views.book, name='book'),
    path('rooms', views.rooms, name='rooms'),
    path('timtable', views.timetable, name='timetable'),
]
