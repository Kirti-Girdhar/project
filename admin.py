from django.contrib import admin

from examapp.models import UserData, question

# Register your models here.

admin.site.register(question)
admin.site.register(UserData)
