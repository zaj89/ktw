"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import index, panel_admin, contact, admin_users_list, admin_mails, admin_events_list, admin_event_detail, \
    admin_email_to_user, admin_delete_declaration, admin_delete_user_verified, admin_event_edit, \
    admin_event_declarations, admin_event_news, admin_event_news_list, admin_event_declarations_form, \
    admin_event_news_new, admin_event_news_del, admin_event_news_edit, admin_event_new
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('panel_admin/', panel_admin, name='panel_admin'),
    path('panel_admin/email_to_user/<int:user_id>/', admin_email_to_user, name='admin_email_to_user'),
    path('panel_admin/', panel_admin, name='panel_admin'),
    path('panel_admin/users/', admin_users_list, name='admin_users_list'),
    path('panel_admin/mails/', admin_mails, name='admin_mails'),
    path('panel_admin/events/', admin_events_list, name='admin_events_list'),
    path('panel_admin/events/new', admin_event_new, name='admin_event_new'),
    path('panel_admin/event/<int:event_id>/', admin_event_detail, name='admin_event_detail'),
    path('panel_admin/event/<int:event_id>/edit/', admin_event_edit, name='admin_event_edit'),
    path('panel_admin/event/<int:event_id>/declarations/', admin_event_declarations, name='admin_event_declarations'),
    path('panel_admin/event/<int:event_id>/declaration/form/<int:user_id>/', admin_event_declarations_form, name='admin_event_declarations_form'),
    path('panel_admin/event/<int:event_id>/news/', admin_event_news, name='admin_event_news'),
    path('panel_admin/event/<int:event_id>/news/list/', admin_event_news_list, name='admin_event_news_list'),
    path('panel_admin/event/<int:event_id>/news/new/', admin_event_news_new, name='admin_event_news_new'),
    path('panel_admin/event/<int:event_id>/news/del/<int:news_id>', admin_event_news_del, name='admin_event_news_del'),
    path('panel_admin/event/<int:event_id>/news/edit/<int:news_id>', admin_event_news_edit, name='admin_event_news_edit'),
    path('panel_admin/event/<int:event_id>/delete_declaration/<int:user_id>/', admin_delete_declaration, name='admin_delete_declaration'),
    path('panel_admin/event/<int:event_id>/delete_user_verified/<int:user_id>/', admin_delete_user_verified, name='admin_delete_user_verified'),
    path('contact/', contact, name='contact'),
    path('account/', include('account.urls')),
    path('', index, name='index'),
    path('event/', include('event.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

