from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task
# from django.http import HttpResponse
# Create your views here.

# Function Based View
# def tasklist(request):
#     return HttpResponse('to do List')

# LogIn View
class LogIn(auth_views.LoginView):
    model = Task
    template_name = 'base/registration/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self) -> str:
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/registration/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    # Register user and route it to ToDo List main page
    # once post request is sent, form_valid method is triggered
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args,**kwargs)

# # LogOut View
# class LogOut(auth_views.LogoutView):
#     model = Task
#     success_url = reverse_lazy('login')

# Class Based View
# ListView - list the tasks from the table task
class TaskList(LoginRequiredMixin, ListView):
    model = Task

    #object_list - tasks in Task model
    # You can change the name of object_list using following method
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['color'] = 'red'
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # title__icontains = will check for the value in tasks
            # other methods - startswith
            context['tasks'] = context['tasks'].filter(
                title__icontains= search_input )
        context['search_input'] = search_input

        return context

# DetailView - gives detail for the task
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task

    context_object_name = 'task'
    template_name = 'base/task.html'

# CreateView - how to create an item
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title','description','complete']
    # alternative - fields = '__all__'
    success_url = reverse_lazy('tasks')  # redirect to url name = tasks

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

# UpdateView - will update the already created task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields =     fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')