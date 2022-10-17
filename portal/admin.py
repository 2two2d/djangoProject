from django.contrib import admin
from .models import User, Project
# Register your models here.
admin.site.register(User)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'img', 'description', 'process_status', 'type_status')
    Actions = None
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

