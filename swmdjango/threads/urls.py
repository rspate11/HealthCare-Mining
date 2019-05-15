from threads import views
from django.conf.urls import url

urlpatterns = [
    url(r'^get-threads/$', views.GetThreads.as_view()),
]
