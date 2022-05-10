from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
import booking.forms as bkf
from django.contrib.auth.models import Group, User
from django.views import View
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
import booking.models as bkm
from django.contrib.auth.decorators import login_required
import cloudinary
from django.utils.datastructures import MultiValueDictKeyError
import datetime
from django.contrib import messages
from django.utils.dateparse import parse_datetime
# Create your views here.


#region helpers
def check_group(logged_user, group):
    return Group.objects.filter(user=logged_user, name=group).exists()


def check_if_owned(logged_user, facil_id):
    pass
#endregion


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


#region Tag
@login_required
def list_tags(request):
    tags = bkm.Tag.objects.all().order_by('id')
    return render(request, 'booking/tag/list_tags.html', {'fac_tags': tags})


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
        return render(request, 'booking/tag/modify_tag.html', {'form': form})

    def post(self, request):
        form = bkf.EditTagForm(request.POST)
        if form.is_valid():
            data = bkm.Tag(shorthand=form.cleaned_data['shorthand'], description=form.cleaned_data['description'])
            data.save()
        return redirect(list_tags)
#endregion


#region Facility

# Have seperate if for each role
@login_required
def display_facility(request):
    if request.user.is_superuser or check_group(request.user, "Admin"):
        facilities = bkm.Facility.objects.all()
        fac_tags = bkm.FacilityTag.objects.all()       
  
    elif check_group(request.user, "Facility Owner"):
        facilities = bkm.Facility.objects.filter(admin=request.user.id)
        owned_facilities = [x.id for x in facilities]
        fac_tags = bkm.FacilityTag.objects.filter(facility_id__in=owned_facilities) 

    else:
        messages.error(request, 'No Access')
        messages.success(request, 'Another Message')
        return redirect(get_booking_index)

    data = []

    for f in facilities:
        data.append((f, fac_tags.filter(facility_id=f.id)))

    return render(request, 'booking/facility/list_facility.html', {'data': data})


class create_facility(LoginRequiredMixin, View):

    permission_required = ('facility.can_create')

    def get(self, request):
        form = bkf.FacilityForm
        return render(request, 'booking/facility/add_facility.html', {'form': form})
        
    def post(self, request):
        form = bkf.FacilityForm(request.POST)

        if form.is_valid():
            data = bkm.Facility(
                admin=User.objects.get(id=request.user.id),
                name=form.cleaned_data['name'],
                postcode=form.cleaned_data['postcode'],
                address=form.cleaned_data['address'],
                indoor=form.cleaned_data['indoor'],
                contact_email=form.cleaned_data['contact_email'],
                contact_phone=form.cleaned_data['contact_phone'],
                image=cloudinary.uploader.upload(request.FILES['image'])['url']
            )

            data.save()
        return redirect(display_facility)


class modify_facility(LoginRequiredMixin, View):
    def get(self, request, facil_id):
        if (bkm.Facility.objects.filter(id=facil_id, admin=request.user.id) or
                request.user.is_superuser or
                check_group(request.user, "Admin")):

            data = bkm.Facility.objects.get(id=facil_id)
            form = bkf.FacilityForm(instance=data)
        else:
            return redirect(get_booking_index)
        return render(request, 'booking/facility/add_facility.html', {'form': form})

    def post(self, request, facil_id):
        if (bkm.Facility.objects.filter(id=facil_id, admin=request.user.id) or
            request.user.is_superuser or check_group(request.user, "Admin")):

            form = bkf.FacilityForm(request.POST)
            if form.is_valid():
                data = bkm.Facility.objects.get(id=facil_id)
                data.name = form.cleaned_data['name']
                data.postcode = form.cleaned_data['postcode']
                data.address = form.cleaned_data['address']
                data.indoor = form.cleaned_data['indoor']
                data.contact_email = form.cleaned_data['contact_email']
                data.contact_phone = form.cleaned_data['contact_phone']
                try:
                    data.image = cloudinary.uploader.upload(request.FILES['image'])['url']
                # No new image to upload
                except MultiValueDictKeyError:
                    pass            
                data.save()
            return redirect(display_facility)
        return redirect(get_booking_index)


class modify_timeslots(LoginRequiredMixin, View):

    def get(self, request, facil_id):
        if (bkm.Facility.objects.filter(id=facil_id, admin=request.user.id) or
            request.user.is_superuser or check_group(request.user, "Admin")):

            # Get all time slots for the facility
            data = bkm.TimeSlot.objects.filter(facility_id=facil_id)

            if(data.count() == 0):
                return render(request, 'booking/timeslots/modify_timeslots.html', { "facil_id": facil_id })

            # create two variables, one with the lowest timedelta and when with a high value
            current = datetime.timedelta(hours=24, minutes=60)
            end = datetime.timedelta(hours=0, minutes=0)

            # loop once for each queryset returned
            for d in data:
                # check if the start value is smaller than the currently recorded one
                _s = datetime.timedelta(hours=d.start.hour, minutes=d.start.minute)
                # if it is, replace it
                if _s < current:
                    current = _s

                # check if the end value is larger than the currently recorded one
                _l = datetime.timedelta(hours=d.end.hour, minutes=d.end.minute)
                # if it is, replace it
                if _l > end:
                    end = _l

            # keep a backup as we will need to start from the lowest again
            original_current = current            

            # This will store the timeslot id for that time
            # [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
            days = [0, 0, 0, 0, 0, 0, 0]
            
            return render(request, 'booking/timeslots/modify_timeslots.html', { "data": list(data.order_by('id')), "facil_id": facil_id })

        return redirect(get_booking_index)

    def post(self, request, facil_id):
        print("hehe")
        if (bkm.Facility.objects.filter(id=facil_id, admin=request.user.id) or
                request.user.is_superuser or
                check_group(request.user, "Admin")):
            returned = request.POST.get('Data').split('|')
        
            data = []

            def parse_bool(val):
                return True

            for r in returned:
                # remove the square brackets on each end of string
                row = r[1:-1]
                row = row.split(',')
                if row[0] == "new":
                    bk = bkm.TimeSlot()
                    bk.facility_id = bkm.Facility.objects.get(id=facil_id)
                    bk.start = parse_datetime("1999-11-23T"+row[1]+":00")
                    bk.end = parse_datetime("1999-11-23T"+row[2]+":00")
                    bk.monday = True if row[3] == "true" else False
                    bk.tuesday = True if row[4] == "true" else False
                    bk.wednesday = True if row[5] == "true" else False
                    bk.thursday = True if row[6] == "true" else False
                    bk.friday = True if row[7] == "true" else False
                    bk.saturday = True if row[8] == "true" else False
                    bk.sunday = True if row[9] == "true" else False
                    bk.save()
                else:
                    current_data = bkm.TimeSlot.objects.get(id=int(row[0]))
                    current_data.start = parse_datetime("1999-11-23T"+row[1]+":00")
                    current_data.end = parse_datetime("1999-11-23T"+row[2]+":00")
                    current_data.monday = True if row[3] == "true" else False
                    current_data.tuesday = True if row[4] == "true" else False
                    current_data.wednesday = True if row[5] == "true" else False
                    current_data.thursday = True if row[6] == "true" else False
                    current_data.friday = True if row[7] == "true" else False
                    current_data.saturday = True if row[8] == "true" else False
                    current_data.sunday = True if row[9] == "true" else False
                    current_data.save()

        return redirect(get_booking_index)


class modify_facility_tags(LoginRequiredMixin, View):

    def get(self, request, facil_id):
        if (bkm.Facility.objects.filter(id=facil_id, admin=request.user.id) or
                request.user.is_superuser or check_group(request.user, "Admin")):

            form_data = bkm.FacilityTag.objects.filter(facility_id=facil_id)
            tags = bkm.Tag.objects.all()

            info_tup = (facil_id, bkm.Facility.objects.get(id=facil_id).name)

            return render(request, 'booking/tag/modify_facility_tags.html', {'data': form_data, 'tags': tags, 'info_tup': info_tup})
        return redirect(get_booking_index)

    def post(self, request, facil_id):
        if (bkm.Facility.objects.filter(id=facil_id, admin=request.user.id) or
                request.user.is_superuser or
                check_group(request.user, "Admin")):

            returned = request.POST.get('Data').split(',')
            returned = list(map(int, returned))

            current = bkm.FacilityTag.objects.filter(facility_id=facil_id)
            current_list = []
            for i in list(current):
                current_list.append(i.tag_id.id)

            # Get all id's that are not in the returned list
            remove = list(set([x for x in current_list if x not in returned]))

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
#endregion


#region Booking
class make_booking(LoginRequiredMixin, View):
    def get(self, request, facil_id):
        # need to remake this as many of it may be irrelevant
        if (bkm.Facility.objects.filter(id=facil_id, admin=request.user.id) or
            request.user.is_superuser or check_group(request.user, "Admin")):

            # Get all time slots for the facility
            data = bkm.TimeSlot.objects.filter(facility_id=facil_id)

            if(data.count() == 0):
                return render(request, 'booking/timeslots/modify_timeslots.html')

            # This will be used in the timetable
            table_data = []

            # We want to populate table_data with every 30minute interval between the earliest slot and the latest
            # So we create two variables, one with the lowest timedelta and when with a high value
            current = datetime.timedelta(hours=24, minutes=60)
            end = datetime.timedelta(hours=0, minutes=0)

            # loop once for each queryset returned
            for d in data:
                # check if the start value is smaller than the currently recorded one
                _s = datetime.timedelta(hours=d.start.hour, minutes=d.start.minute)
                # if it is, replace it
                if _s < current:
                    current = _s

                # check if the end value is larger than the currently recorded one
                _l = datetime.timedelta(hours=d.end.hour, minutes=d.end.minute)
                # if it is, replace it
                if _l > end:
                    end = _l

            # keep a backup as we will need to start from the lowest again
            original_current = current            

            # This will store the timeslot id for that time
            # [Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday]
            days = [0, 0, 0, 0, 0, 0, 0]

            # Add a new time to table_data for every 30min interval between earliest and latest times
            while current != end:
                table_data.append([current, days[0], days[1], days[2], days[3], days[4], days[5], days[6]])
                current = current + datetime.timedelta(minutes=30)
            table_data.append([current, days[0], days[1], days[2], days[3], days[4], days[5], days[6]])

            # This places the timeslot id in the correct position in the days array
            def lay_table(num):
                # read loop below before reading these comments

                # (ret is defined before lay_table call in loop below)
                # Get the start and end time of the current slot
                _e = ret[0].end.time()
                _s = ret[0].start.time()

                # Turn those times into timedeltas
                e = datetime.timedelta(hours=_e.hour, minutes=_e.minute)
                s = datetime.timedelta(hours=_s.hour, minutes=_s.minute)

                # Loop once foreach 30min interval between the start and end
                for j in range(int((e - s)/datetime.timedelta(minutes=30))+1):
                    # If a value is already in that slot, place a "|" and then the value,
                    #   as that will the end of the previous slot and start of the next
                    if table_data[i + j][num] != 0:
                        table_data[i + j][num] = str(table_data[i + j][num]) + "|" + str(ret[0].id)
                    # If not then just place the id
                    else:
                        table_data[i + j][num] = ret[0].id

            # reset the earliest point for next loop
            current = original_current
            for i, k in enumerate(table_data):
                days = [0, 0, 0, 0, 0, 0, 0]

                # Get a timeslot with the same start as current
                ret = data.filter(start__time=str(current))
                
                # If a timeslot was found
                if ret:
                    # Check if timeslot is active on each day of the week
                    # If it is, then run lay_table
                    if ret[0].monday:
                        lay_table(1)
                    if ret[0].tuesday:
                        lay_table(2)
                    if ret[0].wednesday:
                        lay_table(3)
                    if ret[0].thursday:
                        lay_table(4)
                    if ret[0].friday:
                        lay_table(5)
                    if ret[0].saturday:
                        lay_table(6)
                    if ret[0].sunday:
                        lay_table(7)

                current = current + datetime.timedelta(minutes=30)

            return render(request, 'booking/timeslots/modify_timeslots.html', {"table_data": table_data})

        return redirect(get_booking_index)

    def post():
        pass
#endregion

