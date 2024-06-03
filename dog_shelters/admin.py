from django.contrib import admin

from dog_shelters.models import Dog, Shelter

admin.site.register(Shelter)
admin.site.register(Dog)# Register your models here.
