from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from booking.forms import SignUpForm
from django.contrib.auth.models import Group
from django.views import View

# Create your views here.


def get_booking_index(request):
    return render(request, 'booking/index.html')


class register_view(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'booking/register.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            user_group = Group.objects.get(name='User') 
            user_group.user_set.add(user)
            return redirect(get_booking_index)
        return render(request, 'booking/register.html', {'form': form})


class login_view(View):
    def get(self, request):
        return render(request, 'booking/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(get_booking_index)
        else:
            return redirect(get_booking_index)   


def logout_view(request):
    logout(request)
    return redirect(get_booking_index)


def edit_tags_view(request):
    return render(request, 'booking/edit_tags.html')
