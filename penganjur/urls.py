from django.conf.urls import include,url
from . import views
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import path

# Only user in group penganjur can use this views
def grp_penganjur(user):
    if user.groups.filter(name__in=['esertaPenganjur']):
        return user.groups.filter(name__in=['esertaPenganjur'])
    else:
        message= "Anda tidak mempunyai akses ke laman ini!"
        raise PermissionDenied

urlpatterns = [
    # url(r'^$',login_required(views.home),name='penganjur_home'),

    ########## Penganjur URLs #################################
    #Main home link
    path('', views.home,name='home'),
    #Main penganjur home link
    path('penganjur/', login_required(views.penganjur_home),name='penganjur_home'),
    #Aktiviti home
    path('penganjur/aktiviti', login_required(views.aktiviti_home),name='aktiviti_home'),
    #Aktiviti json 
    path('penganjur/aktiviti/json', login_required(views.aktiviti_json.as_view()),name='json_aktiviti'),
    # path('penganjur/aktiviti/json', user_passes_test(grp_penganjur,views.aktiviti_json.as_view()),name='json_aktiviti'),
    #Aktiviti tambah 
    path('penganjur/aktiviti/new', login_required(views.aktiviti_new),name='aktiviti_new'),
    #Aktiviti kemaskini
    path('penganjur/aktiviti/<int:pk>/edit', login_required(views.aktiviti_edit), name='aktiviti_edit'),
    #Aktiviti hapus
    path('penganjur/aktiviti/<int:pk>/remove', login_required(views.aktiviti_remove), name='aktiviti_remove'),
    #Aktiviti detail
    path('penganjur/aktiviti/<int:pk>/', login_required(views.aktiviti_detail), name='aktiviti_detail'),
    #Aktiviti jemputan
    path('penganjur/aktiviti/jemput/<int:pk>/', login_required(views.aktiviti_jemput), name='aktiviti_jemput'),
    ###########################################################
]