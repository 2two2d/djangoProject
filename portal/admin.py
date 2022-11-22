from django.contrib import admin
from .models import User, Project, Category
# Register your models here.
admin.site.register(User)
admin.site.register(Project)
admin.site.register(Category)


