from django.urls import path
from .views import event_detail, events_list, event_declare, event_undeclare, event_exit, event_info, car_declare, \
    car_panel, car_undeclare, set_chair, chair_declare, chair_undeclare, event_news, chat_event_all_message

urlpatterns = [
    path('event_detail/<int:id>/declare', event_declare, name='event_declare'),
    path('event_detail/<int:id>/undeclare', event_undeclare, name='event_undeclare'),
    path('event_detail/<int:id>/event_exit', event_exit, name='event_exit'),
    path('event_detail/<int:id>/event_info', event_info, name='event_info'),
    path('set_chair/<int:id>/', set_chair, name='set_chair'),
    path('<int:eventid>/chair_declare/<int:car_id>/', chair_declare, name='chair_declare'),
    path('<int:eventid>/chair_undeclare/<int:car_id>/', chair_undeclare, name='chair_undeclare'),
    path('car_declare/<int:id>/', car_declare, name='car_declare'),
    path('car_undeclare/<int:id>/', car_undeclare, name='car_undeclare'),
    path('car_panel/<int:id>', car_panel, name='car_panel'),
    path('event_detail/<int:id>/', event_detail, name='event_detail'),
    path('event_detail/<int:id>/chat', chat_event_all_message, name='chat_event_all_message'),
    path('event_news/<int:id>/', event_news, name='event_news'),
    path('events_list/', events_list, name='events_list'),


]