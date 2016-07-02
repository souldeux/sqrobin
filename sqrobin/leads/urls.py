from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.lead_list_view, name='leadlist'),
    url(r'^form/$', views.lead_create_edit_view, name='leadform'),
    url(r'^api/1-0/$', views.lead_creation_api_endpoint_1_0, name='apicreatelead')
    ]