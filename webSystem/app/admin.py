from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Sensor)
admin.site.register(Pavilion)
admin.site.register(Person_Group)
admin.site.register(FarmProperty)
admin.site.register(Person)
admin.site.register(ControlBoard)
admin.site.register(Row)
admin.site.register(WeatherData)
admin.site.register(AjustStatusNew)
admin.site.register(AjustTempNew)
admin.site.register(RowDefaultConf)