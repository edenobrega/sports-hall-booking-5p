from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import booking.forms as bkf
from django.contrib.auth.models import Group, User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import booking.models as bkm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import cloudinary
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
    tags = bkm.Tag.objects.all().order_by('id')
    return render(request, 'booking/tag/list_tags.html', {'fac_tags': tags})


class modify_facility_tags(LoginRequiredMixin, View):

    def get(self, request, facil_id):
        form_data = bkm.FacilityTag.objects.filter(facility_id=facil_id)
        tags = bkm.Tag.objects.all()

        return render(request, 'booking/tag/modify_facility_tags.html', {'data': form_data, 'tags':tags})

    # @csrf_protect
    def post(self, request, facil_id):
        returned = request.POST.get('Data').split(',')
        returned = list(map(int, returned))

        current = bkm.FacilityTag.objects.filter(facility_id=facil_id)
        current_list = []
        for i in list(current):
            current_list.append(i.tag_id.id)
        
        # Get all id's that are not in the returned list
        remove = [x for x in current_list if x not in returned]

        # Get those that are not in current but are in returned
        add = list(set(returned) - set(current_list))

        for r in remove:
            bkm.FacilityTag.objects.filter(facility_id=facil_id, tag_id=r).delete()

        for a in add:
            tg = bkm.Tag.objects.get(id=a)
            fac = bkm.Facility.objects.get(id=facil_id)
            new = bkm.FacilityTag(facility_id=fac, tag_id=tg)
            new.save()


        return redirect(get_booking_index)

class edit_tag(PermissionRequiredMixin, View):

    permission_required = ('tag.can_edit')

    def get(self, request, tag_id):
        data = bkm.Tag.objects.get(id=tag_id)
        form = bkf.EditTagForm(instance=data)
        return render(request, 'booking/tag/modify_tag.html', {'form': form})

    def post(self, request, tag_id):
        form = bkf.EditTagForm(request.POST)
        if form.is_valid():
            data = bkm.Tag.objects.get(id=tag_id)
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


@login_required
def display_facility(request):
    facilities = bkm.Facility.objects.all()
    return render(request, 'booking/facility/list_facility.html', {'facilities': facilities})


class create_facility(LoginRequiredMixin, View):

    permission_required = ('facility.can_create')

    def get(self, request):
        form = bkf.FacilityForm
        return render(request, 'booking/facility/add_facility.html', {'form': form})
        
    def post(self, request):
        form = bkf.FacilityForm(request.POST)

        if form.is_valid():
            data = bkm.Facility(
                admin = User.objects.get(id=request.user.id),
                name = form.cleaned_data['name'],
                postcode = form.cleaned_data['postcode'],
                address = form.cleaned_data['address'],
                indoor = form.cleaned_data['indoor'],
                contact_email = form.cleaned_data['contact_email'],
                contact_phone = form.cleaned_data['contact_phone'],
                image = cloudinary.uploader.upload(request.FILES['image'])['url']
            )

            data.save()
        return redirect(display_facility)



