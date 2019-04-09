from django.conf.urls import url
from users import views

urlpatterns = [
    url(r'^$', views.crime_list),
    url(r'^(?P<pk>[0-9]+)$', views.crime_detail),
    url(r'^ca/(?P<ca>[0-9]+)/$', views.crime_list_ca),
]