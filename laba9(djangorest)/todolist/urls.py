from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
# from .views import TasklistCreateView, TasklistDetailsView, TaskCreateView, TaskDetailsView, TaskTypeCreateView, UserList, UserDetails
from .views import *
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = {
    url(r'^todolists/$', TasklistCreateView.as_view(), name="lists"), # список списков задач
    url(r'^todolists/(?P<pk>[0-9]+)/$', TasklistDetailsView.as_view(), name="list-detail"), #конкретный список задач
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/$', TaskCreateView.as_view(), name="tasks"), # задачи у данного списка
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', TaskDetailsView.as_view(), name="task-detail"),# конкретная задача
    url(r'^tags/$', TaskTypeCreateView.as_view(), name="tags"),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetails.as_view()),
}

urlpatterns = format_suffix_patterns(urlpatterns)

