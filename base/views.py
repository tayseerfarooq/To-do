from django.shortcuts import render,redirect
from django.views.generic.list import ListView #class based views
from django.views.generic.detail import DetailView #Detail about the tasks
from .models import Task
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView

from django.urls import reverse_lazy #reverse method

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm #creating user
from django.contrib.auth import login #redirect already login

# Create your views here.
#We use LoginRequiredMixin to not let any user access the todo if they are not logged in 

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            return super().form_valid(form) #new users register page is added

        

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks') #after the user is authenticated ,the user is redirected to the task list
        return super(RegisterPage, self).get(*args, **kwargs)




class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name='tasks'

    def get_context_data(self,**kwargs): #this function will allow  user to have their own data 
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user) 
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or '' #the main backend for search button used in task_list.html
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__startswith=search_input) #filter the tasks with the first word

        context['search_input'] = search_input #this doesnt refresh the page when searching
        return context
        


class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name='task'
    template_name = 'base/task.html' #change the name of the template for html


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title', 'description', 'complete' ] 
    success_url = reverse_lazy('tasks')

    def form_valid(self,form):
        form.instance.user = self.request.user #only logged in user can add their own tasks
        return super(TaskCreate,self).form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model= Task
    fields= '__all__' #takes in all
    success_url= reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin,DeleteView):
    model=Task
    context_object_name='task'
    success_url=reverse_lazy('tasks')




