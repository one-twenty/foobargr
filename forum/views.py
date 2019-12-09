from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.http import HttpRequest
# from .form import RegisterForm
#from django.contrib import messages


def homepage(request):
    return render(request, 'forum/index.html')


def register(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            login(request, user)
            return redirect('forum:homepage')
        # else:
        #     for msg in form.error_messages:
        #         print(form.error_messages[msg])
        #     return render(request=request,
        #                   template_name="forum/register.html",
        #                   context={"form": form})
    
    form = UserCreationForm
    return render(request, 'forum/register.html', {'form': form})


def logout_request(request: HttpRequest):
    logout(request)
    #messages TODO
    return redirect('forum:homepage')

def login_request(request: HttpRequest):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    form = AuthenticationForm()
    return render(request, 'forum/login.html', {'form': form})
                