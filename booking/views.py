from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, authenticate, logout
from booking.forms import SignUpForm

# Create your views here.

def get_booking_index(request):
    return render(request, 'booking/index.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(get_booking_index)
    else:
        form = SignUpForm()
    return render(request, 'booking/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect(get_booking_index)

def login_view(request):
    if request.method == 'GET':
        return render(request, 'booking/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(get_booking_index)
    else:
        return redirect(get_booking_index)
