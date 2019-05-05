from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^$', views.crime_list),
    url(r'^(?P<pk>[0-9]+)$', views.crime_detail),
    url(r'^ca/(?P<ca>[0-9]+)/$', views.crime_list_ca),
    url(r'^user/', views.get_user_info),
    url(r'^user/register', views.register),
    url(r'^user/login', views.crime_login),
    url(r'^user/logout', views.crime_logout)
]
