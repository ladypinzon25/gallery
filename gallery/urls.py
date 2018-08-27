from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^media/$', views.all_media, name="All media"),
    url(r'^users/$', views.all_users, name="All users"),
    url(r'^modify/$', views.modify, name="Modify"),
    url(r'^create/$', views.create, name="Create"),

]
