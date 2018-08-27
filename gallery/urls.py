from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^media/$', views.all_media, name="All media"),
    url(r'^users/$', views.all_users, name="All users"),
    url(r'^user/(?P<user_id>\d+)/$', views.user_by_id, name="User by id"),
]
