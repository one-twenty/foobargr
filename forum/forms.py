from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Topic, Category, Post


class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(RegisterForm, self).__init__(*args, **kwargs)

    email = forms.EmailField(max_length=254, help_text='Απαραίτητο.')
    username = UsernameField(label='Όνομα Χρήστη')
    password1 = forms.CharField(label='Κωδικός', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Επιβεβαίωση Κωδικού', widget=forms.PasswordInput)
    error_messages = {
        'password_mismatch': 'Εισάγετε ίδιους Κωδικούς',
        'duplicate_username': 'Το Όνομα Χρήστη χρησιμοποιείται ήδη',
        'duplicate_email': 'Το Email χρησιμοποιείται ήδη',
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
            raise ValidationError([self.error_messages['duplicate_username'], self.error_messages['duplicate_email']])
        if User.objects.filter(email=email).exists():
            raise ValidationError(self.error_messages['duplicate_email'], code='duplicate_email')
        if User.objects.filter(username=username).exists():
            raise ValidationError(self.error_messages['duplicate_username'], code='duplicate_username')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(LoginForm, self).__init__(*args, **kwargs)

    username = UsernameField(label='Όνομα Χρήστη')
    password = forms.CharField(label='Κωδικός', widget=forms.PasswordInput)


class TopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['category'] = forms.ModelChoiceField(
                    queryset=Category.objects.filter(parent_category__isnull=False), empty_label=None, label='Κατηγορία')

    class Meta:
        model = Topic
        fields = ('title', 'category', 'content')
        labels = {
            'title': 'Τίτλος',
            'content': ''
        }
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'content'}  
        labels = {'content': ''}
