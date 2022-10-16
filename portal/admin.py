from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Project)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('author')
    Actions = None
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()