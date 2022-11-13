from .models import User, Project, Category
from django import forms
from django.core.validators import RegexValidator, EmailValidator
from django.core.validators import FileExtensionValidator
from django.core.files.images import get_image_dimensions
class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput,
                               validators=[RegexValidator(r'[a-zA-Z\-]', 'В логине доступны только латинские символы')],
                               required=True)

    full_name = forms.CharField(label='ФИО', widget=forms.TextInput,
                                validators=[RegexValidator(r'[а-яА-ЯёЁ\-\s]',
                                                           'В ФИО доступна только кириллица, пробелы и дефис')],
                                required=True)

    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput, required=True,
                             validators=[EmailValidator('Email не верен')])
    checkbox = forms.CharField(label='Privet information permission', widget=forms.CheckboxInput,
                               required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_checkbox(self):
        cd = self.cleaned_data
        print(cd['checkbox'])
        if cd['checkbox'] == False:
            raise forms.ValidationError('Подтвердите обработку персональных данных')
        return cd['checkbox']


class ApplicationCreateForm(forms.ModelForm):
    def file_size(value):
        limit = 2 * 1024 * 1024
        if value.size > limit:
            raise forms.ValidationError('File too large. Size should not exceed 2 MiB.')

    title = forms.CharField(label='Название', widget=forms.TextInput)
    description = forms.CharField(label='Описание', widget=forms.Textarea)
    img = forms.ImageField(label='Изображение', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']), file_size], required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Категория')

    def clean_img(self):
        cd = self.cleaned_data
        if not cd['img']:
            cd['img'] = 'img/default_img.png'
        return cd['img']

    class Meta:
        model = Project
        fields = ('title', 'description', 'img', 'category')

class AddImgForm(forms.ModelForm):
    def file_size(value):
        limit = 2 * 1024 * 1024
        if value.size > limit:
            raise forms.ValidationError('File too large. Size should not exceed 2 MiB.')

    img = forms.ImageField(label='Изображение готового интерьера', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp']), file_size], required=False)

    def clean_img(self):
        cd = self.cleaned_data
        if not cd['img']:
            raise forms.ValidationError('Вы не прикрепили изображение!')
        return cd['img']
    class Meta:
        model = Project
        fields = ('img',)

class AddComForm(forms.ModelForm):
    com = forms.CharField(label='Добавить комментарий', widget=forms.Textarea)

    def clean_img(self):
        cd = self.cleaned_data
        if not cd['com']:
            raise forms.ValidationError('Вы не написали комментарий!')
        return cd['com']
    class Meta:
        model = Project
        fields = ('com',)

class CreateCategoryForm(forms.ModelForm):
    type = forms.CharField(label='Название новой категории', widget=forms.TextInput)

    class Meta:
        model = Category
        fields = ('type',)