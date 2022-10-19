from django.shortcuts import render
from .forms import UserRegistrationForm, ApplicationForm
from django.http import Http404, HttpResponseRedirect, HttpResponse
from .models import User
from .models import Project
from django.views import generic
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


class create_project(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = ['name', 'description', 'status_type', 'img']
    success_url = reverse_lazy('my_projects')
    form_class = ApplicationForm
    template_name = 'user_project_managment/create_project.html'

    def form_valid(self, form):
        fields = form.save(commit=True)
        fields.author = self.request.user
        fields.save()
        return super().form_valid(form)

class my_projects(LoginRequiredMixin, generic.ListView):
    model = Project
    template_name = 'user_project_managment/my_projects.html'
    context_object_name = 'Projects'
    paginate_by = 10

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user.id)

class ProjectDetail(generic.DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'user_project_managment/project_detail.html'
class ProjectDelete(generic.DeleteView):
    model = Project
    template_name = 'user_project_managment/delete_success.html'

    def get_object(self, queryset=None):
        """
        Check the logged in user is the owner of the object or 404
        """
        record = super(ProjectDelete, self).get_object(queryset)
        if record.type_status == 'n':
            if record.Auther != self.request.user:
                raise Http404("You don't own this object")

            return record



