from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^signin$', views.signin, name = 'signin'),
    url(r'^register$', views.register, name = 'register'),
    url(r'^dashboard$', views.dashboard, name = 'dashboard'),
    url(r'^users/create$', views.new, name = 'create'),
    url(r'^users/edit$', views.profile, name = 'profile'),
    url(r'^users/show/(?P<id>\d+)$', views.show, name = 'show'),
    url(r'^users/edit/(?P<id>\d+)$', views.edit, name = 'edit'),
    url(r'^logout$', views.logout, name = 'logout'),
    url(r'^destroy$', views.destroy, name = "destroy")
]
