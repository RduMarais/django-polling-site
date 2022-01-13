from django.urls import path

from . import views
from django.websocket.urls import websocket

app_name = 'poll'  # NOTE registering the namespace

urlpatterns = [
	# ex: /poll/
	path('', views.index, name='index'),
	path('<int:meeting_id>/meeting/', views.meeting, name='meeting'),
	path('<int:meeting_id>/login/', views.login, name='login'),
	path('<int:question_id>/results/', views.results, name='results'),
	path('<int:question_id>/vote/', views.vote, name='vote'),
	path('<int:question_id>/add/', views.add, name='add'),
	path('<int:question_id>/added/', views.added, name='added'),
	websocket("ws/", views.websocket_testview),
]
