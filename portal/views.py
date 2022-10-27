from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .models import User
from .models import Project
from django.views.generic import CreateView, DetailView, ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


# Create your views here.

def main_page(request):
    return render(request, 'main_page.html')


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


class create_project(CreateView):
    model = Project
    fields = ('name', 'description', 'type_status', 'img')
    success_url = reverse_lazy('my_projects')
    template_name = 'user_project_managment/create_project.html'
    context_object_name = 'projects'

    def form_valid(self, form):
        fields = form.save(commit=True)
        fields.author = self.request.user
        fields.save()
        return super().form_valid(form)

class my_projects(ListView):
    model = Project
    template_name = 'user_project_managment/my_projects.html'
    context_object_name = 'Projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)

class ProjectDetail(DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'user_project_managment/project_detail.html'

class ProjectDeleteConfirm(DeleteView):
    model = Project
    template_name = 'user_project_managment/delete_confirm.html'
    success_url = reverse_lazy('my_projects')
    def from_valid(self):
        if self.object.status != 'new':
            return redirect('delete_error')
        else:
            self.object.delete()
            success_url = reverse_lazy('my_projects')
            success_msg = 'Запись удалена'
            return HttpResponseRedirect(success_url, success_msg)

def delete_error(request):
    return render(request, 'user_project_managment/delete_error.html')



