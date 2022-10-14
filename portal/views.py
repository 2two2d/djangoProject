from django.shortcuts import render
from .forms import UserRegistrationForm
from .models import User
from .models import Project

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

def create_project(request):
    model =
    return render(request, 'user_project_managment/create_project.html')

def my_projects(request):
    return render(request, 'user_project_managment/my_projects.html')

