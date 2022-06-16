from django.urls import path
from .views import MessageApiView,index


app_name = 'schedule'
urlpatterns = [
    path('callback', MessageApiView.as_view()),
    path("index", index, name="index"),

]


