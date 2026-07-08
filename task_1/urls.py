from django.urls import path
from .views import *

urlpatterns=[
    path("shrt/<str:shortlink>/", redirect_to_longurl, name="redirect_url" ),
    

]