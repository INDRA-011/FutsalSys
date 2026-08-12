from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect, render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post_login_redirect")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def post_login_redirect(request):
    if request.user.is_staff:
        return redirect("manager_dashboard")
    return redirect("browse_slots")

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # or your custom form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Make sure this redirects on success
        else:
            print("REGISTER ERRORS:", form.errors)  # <-- ADD THIS LINE
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # 'data=' is required!
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Make sure this redirects on success
        else:
            print("LOGIN ERRORS:", form.errors)  # <-- ADD THIS LINE
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})