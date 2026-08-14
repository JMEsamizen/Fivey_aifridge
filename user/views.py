from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from datetime import datetime
from django.contrib import messages

from .models import Profile


class Mainpageview(View):

    def get(self, request):
        context = {}

        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
            except Profile.DoesNotExist:
                profile = None

            context["profile"] = profile

            if profile and profile.birth_date:
                today = timezone.localdate()
                if (today.month, today.day) == (
                    profile.birth_date.month,
                    profile.birth_date.day,
                ):
                    context["is_birthday"] = True

        return render(request, "mainpage.html", context)


class MarketsView(View):

    def get(self, request):
        return render(request, "user/markets.html")


class RegisterView(View):

    def get(self, request):
        return render(request, "user/register.html")

    def post(self, request):

        full_name = request.POST.get("full_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        re_password = request.POST.get("re-password", "")

        if not full_name:
            messages.error(request, "Full name is required")
            return redirect("register")

        if len(full_name) < 2:
            messages.error(request, "Full name must contain at least 2 characters")
            return redirect("register")

        if len(full_name) > 150:
            messages.error(request, "Full name is too long")
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

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.first_name = full_name
        user.save()

        Profile.objects.create(
            user=user,
            full_name=full_name
        )

        login(request, user)

        messages.success(
            request,
            f"Welcome to Fivey, {full_name}! "
            "Add your date of birth on your profile page and we'll "
            "remember to celebrate your birthday with you.",
        )

        return redirect("mainpage")


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return render(request, "user/profile.html", {"profile": profile})

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)

        full_name = request.POST.get("full_name", "").strip()
        birth_date = request.POST.get("birth-date", "").strip()

        if full_name and len(full_name) < 2:
            messages.error(
                request,
                "Full name must contain at least 2 characters",
            )
            return redirect("profile")

        if len(full_name) > 150:
            messages.error(request, "Full name is too long")
            return redirect("profile")

        parsed_birth_date = None

        if birth_date:
            try:
                parsed_birth_date = datetime.strptime(
                    birth_date,
                    "%Y-%m-%d",
                ).date()
            except ValueError:
                messages.error(request, "Invalid birth date")
                return redirect("profile")

            if parsed_birth_date > timezone.localdate():
                messages.error(
                    request,
                    "Birth date cannot be in the future",
                )
                return redirect("profile")

        profile.user.first_name = full_name or request.user.username
        profile.user.save()

        profile.full_name = full_name or None
        profile.birth_date = parsed_birth_date
        profile.save()

        messages.success(request, "Profile updated successfully")
        return redirect("profile")


class LoginView(View):

    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        next_url = request.POST.get("next", "")

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

        profile, _ = Profile.objects.get_or_create(user=user)

        if profile.birth_date:
            today = timezone.localdate()
            if (today.month, today.day) == (
                profile.birth_date.month,
                profile.birth_date.day,
            ):
                messages.success(
                    request,
                    f"Happy birthday, {user.first_name or user.username}! "
                    "Wishing you a wonderful day from all of us at Fivey.",
                )
        else:
            messages.info(
                request,
                "Add your date of birth on your profile page so we can "
                "wish you a happy birthday each year.",
            )
        if url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect("mainpage")


class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("mainpage")
