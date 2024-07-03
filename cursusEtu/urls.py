from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from cursusEtu import views


urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('admin/', admin.site.urls),
    path('Etudiant/',include('Etudiant.urls')),
    path('Note/',include('Note.urls')),
    path('UE/',include('UE.urls')),
    path('Matiere/',include('Matiere.urls')),
    path('Semestre/',include('Semestre.urls')),
    path('^Diplome/',include('Diplome.urls')),
    path('^Annee/',include('Annee.urls')),
    path('Documents/',include('Documents.urls')),
    path('aides', views.aides, name='aides'),
    path('onAdmin', views.onAdmin, name='onAdmin'),
]
