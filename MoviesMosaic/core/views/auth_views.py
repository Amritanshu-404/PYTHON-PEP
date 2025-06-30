import re
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("entertainment")
        messages.error(request, "Invalid username or password")
    return render(request, "Login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        context = {"username": username, "email": email}

        if not re.match(r"^[A-Za-z ]+$", username):
            messages.error(request, "Username must contain alphabetic characters only.")
            return render(request, "Signup.html", context)

        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
            messages.error(request, "Enter a valid email address.")
            return render(request, "Signup.html", context)

        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", password):
            messages.error(
                request,
                "Password must be at least 8 characters and include uppercase, lowercase, and a number.",
            )
            return render(request, "Signup.html", context)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "Signup.html", context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "Signup.html", context)

        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("/")

    return render(request, "Signup.html")
