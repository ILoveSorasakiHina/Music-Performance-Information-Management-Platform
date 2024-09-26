from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render, redirect
from django.views import View


class RegisterView(View):
    def get(self, request: WSGIRequest):
        form = UserCreationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request: WSGIRequest):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request: WSGIRequest):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request: WSGIRequest):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('operation')
        return render(request, 'login.html', {'form': form})


class LogoutView(View):
    def get(self, request: WSGIRequest):
        logout(request)
        return redirect('login')
