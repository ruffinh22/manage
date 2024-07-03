#-*- coding: utf-8 -*-

from django.contrib import admin
from Semestre.models import Semestre, InstanceSemestre

# Register your models here.
admin.site.register(Semestre)
admin.site.register(InstanceSemestre)
