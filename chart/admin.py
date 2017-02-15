from django.contrib import admin
from .models import Schedule, Resource, Task, Roles
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory
# Register your models here.

class TaskAdmin(TreeAdmin):
    form = movenodeform_factory(Task)

admin.site.register(Schedule)
admin.site.register(Resource)
admin.site.register(Task)
admin.site.register(Roles)

