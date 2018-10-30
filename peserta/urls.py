from django.conf.urls import include,url
from . import views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path

urlpatterns = [
    
    #Senarai aktiviti yang belum daftar(json) 
    path('senblmdaftar/json', login_required(views.senarai_blmdaftar_json.as_view()),name='senarai_blmdaftar_json'),
    
    ###########################################################
]