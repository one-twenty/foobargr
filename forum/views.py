from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest, Http404
from .forms import RegisterForm, LoginForm, TopicForm, PostForm
from django.contrib import messages
from .models import Category, Topic, UserProfile, Post
from django.contrib.auth.models import User


def homepage(request):
    return render(request, 'forum/topics.html', {'topics': Topic.objects.all().order_by('-datetime')})


def register_request(request: HttpRequest):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = UserProfile()
            profile.user = user
            profile.save()
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
        return render(request, 'forum/topics.html', {'category': cat, 'topics': topics})
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
                profile = request.user.userprofile
                profile.posts_count += 1
                profile.save()
                return redirect('forum:topic', form.id)  
        form = TopicForm
        return render(request, 'forum/create-topic.html', {'form': form})
    raise Http404


def topic_request(request, topicID):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.topic = Topic.objects.get(id=topicID)
            form.save()
            profile = request.user.userprofile
            profile.posts_count += 1
            profile.save()
            return redirect('forum:topic', topicID)
    try:
        topic = Topic.objects.get(id=topicID)
        posts = Post.objects.filter(topic=topic.id)
        form = PostForm
        return render(request, 'forum/topic.html', {'topic': topic, 'posts': posts, 'form': form})
    except Topic.DoesNotExist:
        raise Http404


def profile_request(request, username):
    try:
        user = User.objects.get(username=username)
        return render(request, 'forum/profile.html', {'requestedUser': user})
    except User.DoesNotExist:
        raise Http404
