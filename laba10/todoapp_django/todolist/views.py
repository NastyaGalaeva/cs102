from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic, View
import requests
from django.http import HttpResponseRedirect
from .forms import TodolistCreateForm, LoginForm, TodolistUpdateForm, TaskCreateForm
from .services import create_auth_header, convert_from_json_to_obj
from .services import generate_confirmation_token
# Create your views here.

def index(request): #Как будет выглядеть главная страница 
    headers = create_auth_header(request.session)
    r = requests.get('http://127.0.0.1:8080/todolists/', headers=headers) #Обращаемся на сервер 
    todolists = r.json()
    return render(request, 'index.html', {'todolists': todolists, 'session': request.session})

class CreateTodolist(View):
    def get(self, request, *args, **kwargs):
        form = TodolistCreateForm()
        return render(request, 'create_todolist.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TodolistCreateForm(request.POST)
        if form.is_valid():
            post_data = {'name': form.cleaned_data['name']}
            headers = create_auth_header(request.session)
            response = requests.post('http://127.0.0.1:8080/todolists/', data=post_data, headers=headers)
            return HttpResponseRedirect('/todolists/')

class ListDetail(View):
    def get(self, request, list_id, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.get('http://127.0.0.1:8080/todolists/{}/'.format(list_id), headers=headers)
        list_details = r.json()
        return render(request, 'list_detail.html', {'list_details': list_details})

class ListDetailDelete(View):
    def get(self, request, list_id, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.delete('http://127.0.0.1:8080/todolists/{}/'.format(list_id), headers=headers)
        return redirect('todolist:index')

class ListDetailUpdate(View):
    def get(self, request, list_id, *args, **kwargs):
        form = TodolistUpdateForm()
        return render(request, 'update_todolist.html', {'form': form, 'list_id': list_id})
    def post(self, request, list_id, *args, **kwargs):
        form = TodolistUpdateForm(request.POST)
        if form.is_valid():
            post_data = {'name': form.cleaned_data['name']}
            headers = create_auth_header(request.session)
            r = requests.put('http://127.0.0.1:8080/todolists/{}/'.format(list_id), headers=headers, data=post_data)
            return redirect('todolist:index')

class TaskCreate(View):
    def get(self, request, list_id, *args, **kwargs):
        form = TaskCreateForm()
        return render(request, 'create_task.html', {'form': form, 'list_id': list_id})
    def post(self, request, list_id, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            post_data = {'name': form.cleaned_data['name'], 'description': form.cleaned_data['description'],
                         'completed': form.cleaned_data['completed'], 'due_date': form.cleaned_data['due_date'],
                         'date_created': form.cleaned_data['date_created'], 'priority': form.cleaned_data['priority'],
                         'tags': form.cleaned_data['tags']}
            headers = create_auth_header(request.session)
            r = requests.post('http://127.0.0.1:8080/todolists/{}/tasks/'.format(list_id), data=post_data, headers=headers)
            return redirect('todolist:list-detail', list_id=list_id)


class TaskUpdate(View):
    def get(self, request, list_id, pk, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.get('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers)
        form = TaskCreateForm(r.json())
        return render(request, 'update_task.html', {'form': form, 'list_id': list_id, 'pk': pk})
    def post(self, request, list_id, pk, *args, **kwargs):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            post_data = {'name': form.cleaned_data['name'], 'description': form.cleaned_data['description'],
                         'completed': form.cleaned_data['completed'], 'due_date': form.cleaned_data['due_date'],
                         'date_created': form.cleaned_data['date_created'], 'priority': form.cleaned_data['priority'],
                         'tags': form.cleaned_data['tags']}
            headers = create_auth_header(request.session)
            r = requests.put('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers, data=post_data)
            return redirect('todolist:list-detail', list_id=list_id)


class TaskDetail(View):
    def get(self, request, list_id, pk, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.get('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers)
        task_details = r.json()
        return render(request, 'task_detail.html', {'task_details': task_details, 'list_id': list_id})

class TaskDetailDelete(View):
    def get(self, request, list_id, pk, *args, **kwargs):
        headers = create_auth_header(request.session)
        r = requests.delete('http://127.0.0.1:8080/todolists/{}/tasks/{}/'.format(list_id, pk), headers=headers)
        return redirect('todolist:list-detail', list_id=list_id)

class LoginView(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            post_data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password']}
            response = requests.post('http://127.0.0.1:8080/api-token-auth/', data=post_data)
            credentials = response.json()
            if credentials.get('token', False):
                request.session['token'] = credentials['token']
                print('token in session')
                print(request.session['token'])
                return HttpResponseRedirect("/todolists/")
            else:
                print('not found token')
                return HttpResponse("You email/password is wrong!", status=403)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        request.session.flush()
        return HttpResponseRedirect('/todolists/')

from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth

class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            post_data = {'username': form.cleaned_data['username'], 'password': form.cleaned_data['password2']}
            response = requests.post('http://127.0.0.1:8080/users/', data=post_data)
            return HttpResponseRedirect('/login')
