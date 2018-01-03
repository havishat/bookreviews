from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),    # This line has changed!
    url(r'^create$', views.create),
    url(r'^login$', views.login), 
    url(r'^logout$', views.logout),
    url(r'^books$', views.books),
    url(r'^addbr$', views.addbr),
    url(r'^users/(?P<id>\d+)$', views.userinfo),
    url(r'^books/add$', views.addbookreview),  
    url(r'^books/(?P<id>\d+)$', views.bookreview),   
    url(r'^books/(?P<id>\d+)/create$', views.createreview)  
]