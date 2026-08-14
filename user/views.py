from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.contrib import messages

from .models import Profile


class Mainpageview(View):

    def get(self, request):
        return render(request, "mainpage.html")


class MarketsView(View):

    def get(self, request):
        return render(request, "user/markets.html")


class RegisterView(View):

    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):

        name = request.POST.get("name", "").strip()
        surname = request.POST.get("surname", "").strip()
        birth_date = request.POST.get("birth-date", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        re_password = request.POST.get("re-password", "")

        if not name:
            messages.error(request, "First name is required")
            return redirect("register")

        if len(name) < 2:
            messages.error(request, "First name must contain at least 2 characters")
            return redirect("register")

        if len(name) > 150:
            messages.error(request, "First name is too long")
            return redirect("register")

        if surname and len(surname) < 2:
            messages.error(request, "Last name must contain at least 2 characters")
            return redirect("register")

        if len(surname) > 30:
            messages.error(request, "Last name is too long")
            return redirect("register")

        if not username:
            messages.error(request, "Username is required")
            return redirect("register")

        if len(username) < 3:
            messages.error(request, "Username must contain at least 3 characters")
            return redirect("register")

        if len(username) > 150:
            messages.error(request, "Username is too long")
            return redirect("register")

        if not username.replace("_", "").isalnum():
            messages.error(
                request,
                "Username can contain only letters, numbers and underscores"
            )
            return redirect("register")

        if User.objects.filter(username__iexact=username).exists():
            messages.error(request, "Username already exists")
            return redirect("register")

        if not email:
            messages.error(request, "Email is required")
            return redirect("register")

        if "@" not in email or "." not in email.split("@")[-1]:
            messages.error(request, "Enter a valid email address")
            return redirect("register")

        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already exists")
            return redirect("register")

        if not password:
            messages.error(request, "Password is required")
            return redirect("register")

        if len(password) < 8:
            messages.error(
                request,
                "Password must contain at least 8 characters"
            )
            return redirect("register")

        if password != re_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        parsed_birth_date = None

        if birth_date:
            try:
                parsed_birth_date = datetime.strptime(
                    birth_date,
                    "%Y-%m-%d"
                ).date()
            except ValueError:
                messages.error(request, "Invalid birth date")
                return redirect("register")

            if parsed_birth_date > timezone.localdate():
                messages.error(
                    request,
                    "Birth date cannot be in the future"
                )
                return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = name
        user.last_name = surname
        user.save()

        Profile.objects.create(
            user=user,
            birth_date=parsed_birth_date,
            surname=surname or None
        )

        login(request, user)

        return redirect("mainpage")


class LoginView(View):

    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        if not username:
            messages.error(request, "Username is required")
            return redirect("login")

        if not password:
            messages.error(request, "Password is required")
            return redirect("login")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        login(request, user)

        return redirect("mainpage")


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("mainpage")
