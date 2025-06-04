from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, LoginForm
from django.http import JsonResponse
from myutils import redirect_with_next


def registration_view(request):
    if (request.method == 'POST'):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.registeruser()
            return redirect('login')
        
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect(reverse('movies-template'))
            else:
                return JsonResponse({'status': 'Failed', 'message': 'Login failed'})
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/login')