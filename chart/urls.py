__author__ = 'sayone-30'
from django.conf.urls import patterns, url
from .views import TaskView
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='gantt.html')),
    url(r'^task/(?P<schedule_id>\d+)/$', TaskView.as_view())
]
