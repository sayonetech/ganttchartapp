import tempfile
import datetime
from .models import Task, Resource


def delete_tasks(tasks):
    for task_data in tasks:
        try:
            task = Task.objects.get(pk=task_data)
            task.delete()
        except:
            pass


def save_task(tasks, schedule):
    task_list = []
    for task_data in tasks:
        try:
            task = Task.objects.get(pk=task_data['id'])
        except:
            task = Task()
        if task_data['depends'] == '':
            # task = Task.objects.create(name=task_data['name'])
            task.parent = None
        else:
            depends = int(task_data['depends'])
            depend_task = tasks[depends-1]
            parent_task = Task.objects.get(name=depend_task['name'])
            task.parent = parent_task
            # get = lambda node_id: Task.objects.get(pk=node_id)
            # parent_task = Task.objects.get(name=depend_task['name'])
            # task = get(parent_task.id).add_child(name=task['name'])
        task.level = task_data.get('level', task.level)
        task.depends = task_data.get('depends', task.depends)
        task.name = task_data.get('name', task.name)
        if schedule:
            task.schedule = schedule
        task.status = task_data.get('status', task.status)
        if task_data['start']:
            start_date = datetime.datetime.fromtimestamp(task_data['start'] / 1e3)
            task.start_date = start_date
        if task_data['start']:
            end_date = datetime.datetime.fromtimestamp(task_data['end'] / 1e3)
            task.end_date = end_date
        task.save()
        if task_data['assigs']:
            for assig in task_data['assigs']:
                resource, created = Resource.objects.get_or_create(id=assig['resourceId'])
                task.resources.add(resource)
        task.duration = task_data.get('duration', task.duration)
        task.is_milestone = task_data.get('startIsMilestone', task.is_milestone)
        task.end_is_milestone = task_data.get('endIsMilestone', task.end_is_milestone)
        try:
            if task_data['file']:
                suffix = "." + task_data['file_name'].split(".")[1]
                f = tempfile.NamedTemporaryFile(prefix=task_data['file_name'], suffix=suffix, dir="media",
                                                delete=False, mode='w')
                f.write(task_data['file'])
                f.flush()
                task.task_file = f.name
        except Exception as e:
            print(e)
        task.save()
        task_list.append(task)
    # serializer = ScheduleSerializer(schedule)
    # return serializer.data
