from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import authenticate

class Mainpageview(View):
    def get(self, request):
      return render(request, 'mainpage.html')

class MarketsView(View):
    def get(self, request):
        return render(request, 'user/markets.html')

class RegisterView(View):

    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):

        name = request.POST.get("name")
        surname = request.POST.get("surname")
        birth_date = request.POST.get("birth-date")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        re_password = request.POST.get("re-password")

        if password != re_password:
            return render(
                request,
                "user/register.html",
                {"error": "Passwords do not match"}
            )

        if User.objects.filter(username=username).exists():
            return render(
                request,
                "user/register.html",
                {"error": "Username already exists"}
            )

        if User.objects.filter(email=email).exists():
            return render(
                request,
                "user/register.html",
                {"error": "Email already exists"}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = name
        user.last_name = surname or ""
        user.save()

        Profile.objects.create(
            user=user,
            birth_date=birth_date if birth_date else None,
            surname=surname
        )

        login(request, user)
        return redirect("mainpage")

class LoginView(View):

    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            return render(
                request,
                "user/login.html",
                {
                    "error": "Invalid username or password"
                }
            )

        login(request, user)

        return redirect("mainpage")

class LogoutView(View):

    def post(self, request):

        logout(request)

        return redirect("mainpage")

    def get(self, request):

        logout(request)

        return redirect("mainpage") 

