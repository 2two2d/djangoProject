from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .models import User
from .models import Project
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.

def main_page(request, pk):
    if pk != 'All':
        Projects = Project.objects.filter(process_status=pk)
    else:
        Projects = Project.objects.all()

    count = Project.objects.filter(process_status='i').count()

    return render(request, 'main_page.html', {'Projects': Projects, 'count_in_process': count})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            return render(request, 'registrations/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registrations/register.html', {'user_form': user_form})


class create_project(CreateView, LoginRequiredMixin):
    model = Project
    fields = ('name', 'description', 'type_status', 'img')
    success_url = reverse_lazy('my_projects', args=('All',))
    template_name = 'user_project_managment/create_project.html'
    context_object_name = 'projects'

    def form_valid(self, form):
        fields = form.save(commit=True)
        fields.author = self.request.user
        fields.save()
        return super().form_valid(form)
@login_required
def my_projects(request, pk):

    if pk != 'All':
        Projects = Project.objects.filter(process_status=pk, author=request.user)
    else:
        Projects = Project.objects.filter(author=request.user)

    count = Project.objects.filter(process_status='i', author=request.user).count()

    return render(request, 'user_project_managment/my_projects.html', {'Projects': Projects, 'count_in_process': count})

class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'user_project_managment/project_detail.html'

class ProjectDeleteConfirm(DeleteView, LoginRequiredMixin):
    model = Project
    template_name = 'user_project_managment/delete_confirm.html'
    success_url = reverse_lazy('my_projects', args=('All',))
    context_object_name = 'project'
    def from_valid(self):
        if self.object.process_status != 'n':
            return redirect('delete_error')
        else:
            self.object.delete()
            success_url = reverse_lazy('my_projects', args=('All',))
            success_msg = 'Запись удалена'
            return HttpResponseRedirect(success_url, success_msg)

def delete_error(request):
    return render(request, 'errors/delete_error.html')
@login_required
def change_status(request):
    if request.user.is_staff:
        Projects = Project.objects.filter(process_status='n')
    else:
        return render(request, 'errors/staff_error.html', {})

    return render(request, 'staff_project_managment/change_status.html', {'Projects': Projects})

def confirm_status_change(request, pk, st):

    Project.get(id=pk).process_status = st
    Project.get(id=pk).save()

    return render(request, '' ,{})

