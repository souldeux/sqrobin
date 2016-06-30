from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.lead_list_view, name='leadlist'),
    url(r'^form/$', views.lead_create_edit_view, name='leadform'),
    ]