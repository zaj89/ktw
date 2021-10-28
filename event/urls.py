from django.urls import path
from .views import event_detail, events_list, event_declare, event_undeclare, event_exit, event_info, car_declare, \
    car_panel, car_undeclare, set_chair, chair_declare, chair_undeclare, event_news, chat_event_all_message, \
    admin_chat_event_del_message, admin_verification_declarations, candidate_acceptance, reject_candidate, \
    chat_with_admin, admin_with_user, admin_chat_priv_del_message, chat_with_admin_del_mess, car_panel_passenger, \
    chat_event_10_messages, chat_car_all_message

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
    path('car_panel/<int:car_id>/chat', chat_car_all_message, name='chat_car_all_message'),
    path('car_panel_passenger/<int:id>', car_panel_passenger, name='car_panel_passenger'),
    path('event_detail/<int:id>/', event_detail, name='event_detail'),
    path('event_detail/<int:event_id>/verification_declarations', admin_verification_declarations, name='admin_verification_declarations'),
    path('event_detail/<int:event_id>/verification_declarations/candidate_acceptance/<int:candidate_id>', candidate_acceptance, name='candidate_acceptance'),
    path('event_detail/<int:event_id>/verification_declarations/reject_candidate/<int:candidate_id>', reject_candidate, name='reject_candidate'),
    path('event_detail/<int:id>/chat10/', chat_event_10_messages, name='chat_event_10_messages'),
    path('event_detail/<int:id>/chat/', chat_event_all_message, name='chat_event_all_message'),
    path('event_detail/<int:user_id>/chat_with_admin/del/<int:mes_id>/', chat_with_admin_del_mess, name='chat_with_admin_del_mess'),
    path('event_detail/<int:id>/chat_with_admin/', chat_with_admin, name='chat_with_admin'),
    path('event_detail/<int:id>/admin_with_user/', admin_with_user, name='admin_with_user'),
    path('event_detail/<int:user_id>/admin_with_user/<int:message_id_to_del>', admin_chat_priv_del_message, name='admin_chat_priv_del_message'),
    path('event_detail/<int:event_id>/chat/<int:message_id_to_del>/', admin_chat_event_del_message, name='admin_chat_event_del_message'),
    path('event_news/<int:id>/', event_news, name='event_news'),
    path('events_list/', events_list, name='events_list'),


]
