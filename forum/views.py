from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, Http404
from .form import RegisterForm, LoginForm, TopicForm
from django.contrib import messages
from .models import Category, Topic


def homepage(request):
    return render(request, 'forum/homepage.html', {'topics': Topic.objects.all().order_by('-datetime')})


def register(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            messages.success(request, 'Επιτυχής εγγραφή')
            login(request, user)
            return redirect('forum:homepage')
        else:
            for value in form.errors:
                messages.error(request, form.errors[value])
    
    form = RegisterForm
    return render(request, 'forum/register.html', {'form': form})


def logout_request(request: HttpRequest):
    logout(request)
    messages.success(request, 'Επιτυχής Αποσύνδεση')
    return redirect('forum:homepage')


def login_request(request: HttpRequest):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                messages.success(request, f'Καλωσόρισες, {username}')
                login(request, user)
                return redirect('forum:homepage')
            else:
                messages.error(request, 'Λάθος Όνομα Χρήστη ή Κωδικός')
        else:
            messages.error(request, 'Λάθος Όνομα Χρήστη ή Κωδικός')
    form = LoginForm
    return render(request, 'forum/login.html', {'form': form})
                

def error_404(request, exception):
    data = {}
    return render(request,'forum/404.html', data)


def category_request(request, category):
    try:
        cat = Category.objects.get(url=category)
        topics = Topic.objects.filter(category=cat.id).order_by('-datetime')
        return render(request, 'forum/category.html', {'category': cat, 'topics': topics})
    except Category.DoesNotExist:
        raise Http404


def create_topic(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = TopicForm(request.POST)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                form.save()
                messages.success(request, 'Το θέμα σας δημιουργήθηκε')
                return redirect('forum:topic', form.id) #TODO redirect to created topic  
        form = TopicForm
        return render(request, 'forum/create-topic.html', {'form': form})
    raise Http404


def topic_request(request, topicID):
    try:
        topic = Topic.objects.get(id=topicID)
        return render(request, 'forum/topic.html', {'topic': topic})
    except Topic.DoesNotExist:
        raise Http404
