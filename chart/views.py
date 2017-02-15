import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.http import JsonResponse, Http404
from .models import Schedule
from .serializers import ScheduleSerializer, ScheduleDetailSerializer
from .utils import save_task, delete_tasks


class TaskView(View):

    def get(self, *args, **kwargs):
        try:
            schedule = Schedule.objects.get(pk=kwargs.get('schedule_id'))
            serializer = ScheduleSerializer(schedule)
        except:
            raise Http404
        return JsonResponse(data={'project': serializer.data,
                                  "schedule_id": kwargs.get('schedule_id'),
                                  'ok': 'ok'},
                            safe=False)

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        try:
            schedule = Schedule.objects.get(pk=kwargs.get('schedule_id'))
        except:
            schedule = ''
        data = json.loads(request.POST['prj'])
        if data['deletedTaskIds']:
            delete_tasks(data['deletedTaskIds'])
        if schedule:
            serializer = ScheduleDetailSerializer(schedule, data=data)
            if serializer.is_valid():
                serializer.save()
            # task_serializer = TaskDetailSerializer(data=data['tasks'])
            # if task_serializer.is_valid():
            #     task_serializer.save()
            save_task(data['tasks'], schedule)
        else:
            serializer = ScheduleDetailSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            save_task(data['tasks'], None)
        try:
            schedule = Schedule.objects.get(pk=kwargs.get('schedule_id'))
            serializer = ScheduleSerializer(schedule)
            return JsonResponse(data={'project': serializer.data, 'ok': 'ok'}, safe=False)
        except:
            raise Http404
