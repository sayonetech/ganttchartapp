import os
from django.db import models
from django.utils.translation import ugettext_lazy as _
from treebeard.mp_tree import MP_Node
from django.contrib.auth.models import AbstractBaseUser

# Create your models here.


def get_new_static_resource_path(instance, filename, folder_name=''):
    return os.path.join(folder_name, filename)


def get_new_task_file_resource_path(instance, filename):
    return get_new_static_resource_path(instance, filename, 'task')


class BaseGanttModel(models.Model):
    """Abstract model that groups some basic fields present in all Gantt Chart models"""
    name = models.CharField(max_length=250, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    duration = models.IntegerField(default=0)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


class Schedule(BaseGanttModel):
    can_write = models.BooleanField(default=True)
    can_write_on_parent = models.BooleanField(default=False)
    selected_row = models.IntegerField(default=0)

    def __str__(self):
        return u'%s' % (
            self.name,
        )


# class MileStone(BaseGanttModel):
#     schedule = models.ForeignKey('Schedule', null=True, blank=True)
#
#     def __unicode__(self):
#         return u'%s' % (
#             self.name,
#         )
class Roles(models.Model):
    name = models.CharField('Name', max_length=30, blank=True)


class Resource(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, _('Male')),
        (FEMALE, _('Female')),
    )
    # Fields

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1,
                              blank=True, null=True)
    role = models.ForeignKey('Roles', null=True, blank=True)
    effort = models.IntegerField(default=0)


class Task(BaseGanttModel):

    parent = models.ForeignKey('self', null=True, blank=True, related_name='children')
    level = models.IntegerField(default=0)
    depends = models.CharField(max_length=300, null=True,blank=True)
    schedule = models.ForeignKey('Schedule', null=True, blank=True)
    is_milestone = models.BooleanField(default=False)
    end_is_milestone = models.BooleanField(default=False)
    resources = models.ManyToManyField('Resource', blank=True)
    status = models.CharField(max_length=300,
                              blank=True, null=True)
    progress = models.DecimalField(decimal_places=2, default=0, max_digits=10)
    task_file = models.FileField(
        upload_to=get_new_task_file_resource_path,
        null=True,
        blank=True,
        verbose_name=_("Task file")
    )

    def __str__(self):
        return 'Task: %s' % self.name




