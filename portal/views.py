from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ApplicationCreateForm, AddImgForm, AddComForm, CreateCategoryForm
from django.http import HttpResponseRedirect
from .models import Project, Category
from django.views.generic import DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


# Create your views here.

def main_page(request):

    Projects = Project.objects.filter(process_status='d')[0:4]

    count = Project.objects.filter(process_status='i').count()

    return render(request, 'main_page.html', {'Projects': Projects, 'count_in_process': count})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'registrations/register_done.html', {'new_user': new_user})

    else:
        user_form = UserRegistrationForm()
    return render(request, 'registrations/register.html', {'user_form': user_form})


def create_project(request):
    if request.method == 'POST':
        if not Category.objects.all():
            return render(request, 'errors/category_error,html')
        else:
            form = ApplicationCreateForm(request.POST, request.FILES)
            if form.is_valid():
                Application = form.save(commit=False)
                Application.author = request.user
                Application.img = form.cleaned_data['img']
                Application.save()
                return redirect(reverse_lazy('my_projects', args=('All',)))
    else:
        form = ApplicationCreateForm()

    return render(request, 'user_project_managment/create_project.html', {'form': form})

    # model = Project
    # fields = ('name', 'description', 'type_status', 'img')
    # success_url = reverse_lazy('my_projects', args=('All',))
    # template_name = 'user_project_managment/create_project.html'
    # context_object_name = 'projects'
    #
    # form_class = ApplicationCreateForm
    #
    # def form_valid(self, form):
    #     fields = form.save(commit=True)
    #     fields.author = self.request.user
    #     fields.save()
    #     return super().form_valid(form)
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

    return render(request, 'staff_project_managment/projects_to_change.html', {'Projects': Projects})

# def projects_to_change(requset):
#     return render(requset, 'staff_project_managment/projects_to_change.html', )


def confirm_status_change(request, pk, st):

    new_Projects = Project.objects.get(id=pk)

    new_Projects.save()

    if st == 'd':
        if request.method == 'POST':
            form = AddImgForm(request.POST, request.FILES)
            if form.is_valid():
                new_Projects.img = form.cleaned_data['img']
                new_Projects.process_status = st
                new_Projects.save()
                return render(request, 'staff_project_managment/change_status_success.html', {'new_Projects':new_Projects})
        else:
            form = AddImgForm()

        return render(request, 'staff_project_managment/change_status.html', {'form': form})


    elif st == 'i':
        if request.method == 'POST':
            form = AddComForm(request.POST)
            if form.is_valid():
                new_Projects.com = form.cleaned_data['com']
                new_Projects.process_status = st
                new_Projects.save()
                return render(request, 'staff_project_managment/change_status_success.html', {'new_Projects':new_Projects})
        else:
            form = AddComForm()

        return render(request, 'staff_project_managment/change_status.html', {'form': form})

def change_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)
        if form.is_valid():
            new_Category = form.save(commit=False)
            new_Category.save()
            return render(request, 'staff_project_managment/create_category_success.html', {})
    else:
        form = CreateCategoryForm()

    categories = Category.objects.all()

    return render(request, 'staff_project_managment/change_category.html', {'form': form, 'categories': categories})

def category_delete(request, pk):
    Category.objects.get(type=pk).delete()
    return render(request, 'staff_project_managment/delete_category_success.html')

