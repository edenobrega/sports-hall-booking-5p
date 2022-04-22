from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import booking.forms as bkf
from django.contrib.auth.models import Group
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from booking.models import Tag
from django.contrib.auth.decorators import login_required
# Create your views here.


def get_booking_index(request):
    return render(request, 'booking/index.html')


class register_view(View):

    def get(self, request):
        form = bkf.SignUpForm()
        return render(request, 'booking/register.html', {'form': form})

    def post(self, request):
        form = bkf.SignUpForm(request.POST)
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


@login_required
def list_tags(request):
    tags = Tag.objects.all().order_by('id')
    return render(request, 'booking/list_tags.html', {'fac_tags': tags})


class edit_tag(PermissionRequiredMixin, View):

    permission_required = ('tag.can_edit')

    def get(self, request, tag_id):
        data = Tag.objects.get(id=tag_id)
        form = bkf.EditTagForm(instance=data)
        return render(request, 'booking/modify_tag.html', {'form': form})

    def post(self, request, tag_id):
        form = bkf.EditTagForm(request.POST)
        if form.is_valid():
            data = Tag.objects.get(id=tag_id)
            data.shorthand = form.cleaned_data['shorthand']
            data.description = form.cleaned_data['description']
            data.save()
        return redirect(list_tags)


class create_tag(LoginRequiredMixin, View):

    permission_required = ('tag.can_create')

    def get(self, request):
        form = bkf.EditTagForm()
        return render(request, 'booking/modify_tag.html', {'form': form})

    def post(self, request):
        form = bkf.EditTagForm(request.POST)
        if form.is_valid():
            data = Tag(shorthand=form.cleaned_data['shorthand'], description=form.cleaned_data['description'])
            data.save()
        return redirect(list_tags)
