from . import views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name':'login.html'}, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page':'home'}, name='logout'),
    url(r'^profiles/', include('profiles.urls', namespace='profiles')),
    url(r'^leads/', include('leads.urls', namespace='leads')),
    url(r'^automations/', include('automations.urls', namespace='automations')),
]
