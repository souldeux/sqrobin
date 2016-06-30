from . import views
from django.conf.urls import url


urlpatterns = [
    #url(r'^$', views.index, name='idunno'),
    url(r'^eal/$', views.email_automation_list_view, name='emailautomationlist'),
    url(r'^pal/$', views.post_automation_list_view, name='postautomationlist'),
    url(r'^eaf/$', views.email_automation_create_edit_view, name='emailautomationform'),
    url(r'^paf/$', views.post_automation_create_edit_view, name='postautomationform'),
    ]