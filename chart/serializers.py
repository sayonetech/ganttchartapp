__author__ = 'sayone-30'
import time
from rest_framework import serializers
from .models import Schedule, Task, Resource, Roles


class RoleSerializer(serializers.Serializer):
    name = serializers.CharField()
    id = serializers.CharField()


class ResourceSerializer(serializers.Serializer):
    name = serializers.SerializerMethodField('make_name')
    resourceId = serializers.SerializerMethodField('get_resource_id')
    id = serializers.SerializerMethodField('get_task_id')
    roleId = serializers.SerializerMethodField('get_role_data')
    effort = serializers.IntegerField(required=False)

    def get_role_data(self, resource):
        return resource.role.id if resource.role else ''

    def get_resource_id(self, resource):
        return resource.pk

    def get_task_id(self, resource):
        return resource.pk

    def make_name(self, resource):
        name = resource.first_name + resource.last_name
        return name


class TaskSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField('get_task_id')
    level = serializers.SerializerMethodField('get_depth')
    depends = serializers.CharField()
    name = serializers.CharField(required=False)
    code = serializers.SerializerMethodField('create_code')
    status = serializers.CharField(required=False)
    canWrite = serializers.BooleanField(required=False)
    start = serializers.SerializerMethodField('get_start_date')
    end = serializers.SerializerMethodField('get_end_date')
    duration = serializers.IntegerField(required=False)
    startIsMilestone = serializers.SerializerMethodField('get_is_milestone')
    endIsMilestone = serializers.BooleanField(required=False)
    collapsed = serializers.BooleanField(required=False)
    assigs = serializers.SerializerMethodField('get_resources_list')
    hasChild = serializers.SerializerMethodField('check_has_child')
    file = serializers.SerializerMethodField('make_file_name')

    def get_task_id(self, task):
        return task.pk

    def get_depth(self, task):
        return task.level

    def create_code(self, task):
        return task.name[:3] + str(task.id)

    def check_has_child(self, task):
        if task.parent:
            return True
        else:
            return False

    def get_start_date(self, task):
        if task.start_date:
            start_date = int(time.mktime(task.start_date.timetuple())*1000)
        else:
            start_date = ''
        return start_date

    def get_end_date(self, task):
        if task.end_date:
            end_date = int(time.mktime(task.end_date.timetuple())*1000)
        else:
            end_date = ''
        return end_date

    def get_is_milestone(self, task):
        return task.is_milestone

    def make_file_name(self, task):
        if task.task_file:
            return "/media"+task.task_file.name.split("media")[1]
        else:
            return ''

    def get_resources_list(self, task):
        resources = task.resources.all()
        resources_serializer = ResourceSerializer(resources, many=True)
        return resources_serializer.data


class TaskDetailSerializer(serializers.Serializer):
    level = serializers.IntegerField()
    name = serializers.CharField(required=False)
    status = serializers.CharField(required=False)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
    duration = serializers.IntegerField(required=False)
    is_milestone = serializers.BooleanField()
    end_is_milestone = serializers.BooleanField(required=False)
    collapsed = serializers.BooleanField(required=False)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Schedule` instance, given the validated data.
        """
        instance.depth = validated_data.get('level', instance.depth)
        instance.name = validated_data.get('name', instance.name)
        instance.status = validated_data.get('status', instance.status)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.duration = validated_data.get('duration', instance.duration)
        instance.is_milestone = validated_data.get('startIsMilestone', instance.is_milestone)
        instance.end_is_milestone = validated_data.get('endIsMilestone', instance.end_is_milestone)
        instance.collapsed = validated_data.get('collapsed', instance.collapsed)
        instance.save()
        return instance


class ScheduleSerializer(serializers.Serializer):
    selectedRow = serializers.IntegerField(required=False)
    canWrite = serializers.SerializerMethodField('get_can_write')
    canWriteOnParent = serializers.SerializerMethodField('get_can_write_on_parent')
    tasks = serializers.SerializerMethodField('get_tasks_data')
    resources = serializers.SerializerMethodField('get_resources_list')
    roles = serializers.SerializerMethodField('get_roles_list')

    def get_can_write(self, schedule):
        return schedule.can_write

    def get_can_write_on_parent(self, schedule):
        return schedule.can_write_on_parent

    def get_tasks_data(self, schedule):
        tasks = Task.objects.filter(schedule=schedule)
        task_serializer = TaskSerializer(tasks, many=True)
        return task_serializer.data

    def get_resources_list(self, schedule):
        resources = Resource.objects.all()
        resources_serializer = ResourceSerializer(resources, many=True)
        return resources_serializer.data

    def get_roles_list(self, schedule):
        roles = Roles.objects.all()
        role_serializer = RoleSerializer(roles, many=True)
        return role_serializer.data


class ScheduleDetailSerializer(serializers.ModelSerializer):
    # id = serializers.ReadOnlyField()
    selectedRow = serializers.IntegerField(required=False)
    canWrite = serializers.BooleanField()
    canWriteOnParent = serializers.BooleanField()
    tasks = TaskDetailSerializer(many=True)

    class Meta:
        model = Schedule

    def create(self, validated_data):
        """
        Create and return a new `Schedule` instance, given the validated data.
        """
        return Schedule.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Schedule` instance, given the validated data.
        """
        instance.selected_row = validated_data.get('selectedRow', instance.selected_row)
        instance.can_write = validated_data.get('canWrite', instance.can_write)
        instance.can_write_on_parent = validated_data.get('canWriteOnParent', instance.can_write_on_parent)
        instance.save()
        return instance