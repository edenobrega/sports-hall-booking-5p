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
from geopy.geocoders import Nominatim
import math
import calendar


#region helpers
# Current Groups:
#   "Admin"
#   "Facility Owner"
#   "User"

def check_group(logged_user, group):
    return Group.objects.filter(user=logged_user, name=group).exists()


# pass request.user to logged_user
def check_if_owned(logged_user, facil_id):
    if (bkm.Facility.objects.filter(id=facil_id, admin=logged_user.id) or
        logged_user.is_superuser or
        check_group(logged_user, "Admin")):

        return True
    return False

# As a method incase i make users who are not super_user able to edit certain pieces of data
#   e.g. only super_user may add or remove tags
def check_if_super(logged_user):
    return logged_user.is_superuser


def get_distance(lat1, lon1, lat2, lon2):
    '''
    Get the distance between two locations
    '''
    def deg2rad(deg):
        return deg * (math.pi/180)

    earth = 6371
    dLat = deg2rad(lat2-lat1)
    dLon = deg2rad(lon2-lon1)

    a = (
        math.sin(dLat/2) * math.sin(dLat/2) +
        math.cos(deg2rad(lat1)) * math.cos(deg2rad(lat2)) *
        math.sin(dLon/2) * math.sin(dLon/2)
        )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = earth * c
    return d / 1.609
#endregion


#region Account
# get_booking_index
class index_view(View):
    def get(self, request):
        form = bkf.SearchForm()
        tags = bkm.Tag.objects.all()
        return render(request, 'booking/index.html', {'form': form, 'tags': tags, 'rows': round(len(tags)/3)})

    def post(self, request):
        form = bkf.SearchForm(request.POST)

        if form.is_valid():
            # Get list of facilities that have the asked for tag
            vals = bkm.FacilityTag.objects.filter(tag_id=form.cleaned_data.get('sports_tag').id)
            vals = [x.facility_id for x in vals]
            
            # Get the center of the radius
            geo = Nominatim(user_agent="bookit_app")
            loc = geo.geocode(query=form.cleaned_data.get('location'), country_codes=["gb"])
            loc = (loc.longitude, loc.latitude)

            radius = int(form.cleaned_data.get('distance'))

            # Get all that are within the radius
            valid = []
            for v in vals:
                if get_distance(loc[1], loc[0], float(v.latitude), float(v.longitude)) <= radius:
                    valid.append(v)
            form = bkf.SearchForm()

            if len(valid) == 0:
                messages.error(request, 'No Results')
            else:
                messages.success(request, f'{len(valid)} Facilities Found')

            return render(request, 'booking/facility/search_results.html', {"returned": valid, "form":form})

        form = bkf.SearchForm()
        return render(request, 'booking/index.html', {'form': form})


# register
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
            if form.cleaned_data['facility_owner']:
                user_group = Group.objects.get(name='Facility Owner')
                user_group.user_set.add(user)
            return redirect('get_booking_index')
        return render(request, 'booking/register.html', {'form': form})


# login_view
class login_view(View):
    def get(self, request):
        return render(request, 'booking/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('get_booking_index')
        else:
            messages.error(request, "Username or Password was incorrect")            
            return redirect('login_view')


# logout_view
def logout_view(request):
    logout(request)
    return redirect('get_booking_index')
#endregion


#region Tag
# list_tags
class list_tags(LoginRequiredMixin, View):
    def get(self, request):
        if check_if_super(request.user):
            tags = bkm.Tag.objects.all().order_by('id')
            return render(request, 'booking/tag/list_tags.html', {'fac_tags': tags})
        return redirect('get_booking_index')

    def post(self, request):
        if check_if_super(request.user):
            data = bkm.Tag.objects.filter(id=request.POST['Data'])
            data.delete()
        messages.success(request, "Successfully deleted tag")
        return redirect('list_tags')


# edit_tag
class edit_tag(LoginRequiredMixin, View):
    def get(self, request, tag_id):
        if check_if_super(request.user):
            data = bkm.Tag.objects.get(id=tag_id)
            form = bkf.EditTagForm(instance=data)
            return render(request, 'booking/tag/modify_tag.html', {'form': form})
        messages.error(request, 'No Access')
        return redirect('get_booking_index')

    def post(self, request, tag_id):
        if check_if_super(request.user):
            form = bkf.EditTagForm(request.POST)
            if form.is_valid():
                data = bkm.Tag.objects.get(id=tag_id)
                data.shorthand = form.cleaned_data['shorthand']
                data.description = form.cleaned_data['description']
                try:
                    data.image = cloudinary.uploader.upload(request.FILES['image'])['url']
                # No new image to upload
                except MultiValueDictKeyError:
                    pass   
                data.save()
            return redirect('list_tags')
        messages.error(request, 'No Access')
        return redirect('get_booking_index')


# create_tag
class create_tag(LoginRequiredMixin, View):
    def get(self, request):
        if check_if_super(request.user):
            form = bkf.EditTagForm()
            return render(request, 'booking/tag/modify_tag.html', {'form': form})
        messages.error(request, 'No Access')
        return redirect('get_booking_index')

    def post(self, request):
        if check_if_super(request.user):
            form = bkf.EditTagForm(request.POST)
            if form.is_valid():
                data = bkm.Tag()
                data.shorthand = form.cleaned_data['shorthand']
                data.description = form.cleaned_data['description']
                try:
                    data.image = cloudinary.uploader.upload(request.FILES['image'])['url']
                # No new image to upload
                except MultiValueDictKeyError:
                    messages.error(request, 'No image was uploaded with Tag')
                    pass   
                data.save()
                messages.success(request, 'Tag successfully created')
            else:
                messages.error(request, 'Failed to create Tag')
            return redirect('list_tags')
        messages.error(request, 'No Access')
        return redirect('get_booking_index')
#endregion


#region Facility
# display_facilities
class display_facility(LoginRequiredMixin, View):
    def get(self, request):
        if check_if_super(request.user) or check_group(request.user, "Admin"):
            facilities = bkm.Facility.objects.all()
            fac_tags = bkm.FacilityTag.objects.all()       
    
        elif check_group(request.user, "Facility Owner"):
            facilities = bkm.Facility.objects.filter(admin=request.user.id)
            owned_facilities = [x.id for x in facilities]
            fac_tags = bkm.FacilityTag.objects.filter(facility_id__in=owned_facilities) 

        else:
            messages.error(request, 'No Access')
            return redirect('get_booking_index')

        data = []

        for f in facilities:
            data.append((f, fac_tags.filter(facility_id=f.id)))

        return render(request, 'booking/facility/list_facility.html', {'data': data})        

    def post(self, request):
        if check_if_super(request.user) or check_group(request.user, "Admin"):
            data = bkm.Facility.objects.filter(id=request.POST["Data"])
            data.delete()
            messages.success(request, 'Successfully deleted Facility')
    
        elif check_group(request.user, "Facility Owner"):
            data = bkm.Facility.objects.filter(admin=request.user.id, id=request.POST["Data"])
            data.delete()
            messages.success(request, 'Successfully deleted Facility')

        else:
            messages.error(request, 'No Access')
            return redirect('get_booking_index')
        return redirect('display_facilities')  


# create_facility
class create_facility(LoginRequiredMixin, View):
    def get(self, request):
        if check_if_super(request.user) or check_group(request.user, "Admin") or check_group(request.user, "Facility Owner"):
            form = bkf.FacilityForm()
            return render(request, 'booking/facility/add_facility.html', {'form': form})
        messages.error(request, 'No Access')
        return redirect('get_booking_index')

    def post(self, request):
        if check_if_super(request.user) or check_group(request.user, "Admin") or check_group(request.user, "Facility Owner"):
            form = bkf.FacilityForm(request.POST)
            if form.is_valid():
                geo = Nominatim(user_agent="bookit_app")
                loc = geo.geocode(query={
                    "street": form.cleaned_data['address'],
                    "postalcode": form.cleaned_data['postcode'],
                    "country": "gb"})
                if not loc:
                    loc = geo.geocode(query={
                        "postalcode": form.cleaned_data['postcode'],
                        "country": "gb"})
                if not loc:
                    # Default to location of code institute :)
                    long = 53.2978186
                    lat = -6.1823261
                else:
                    long = loc.longitude
                    lat = loc.latitude

                try:
                    _image = cloudinary.uploader.upload(request.FILES['image'])['url']
                # No new image to upload
                except MultiValueDictKeyError:
                    messages.error(request, 'No image was supplied')
                    _image = None

                data = bkm.Facility(
                    admin=request.user,
                    name=form.cleaned_data['name'],
                    postcode=form.cleaned_data['postcode'],
                    address=form.cleaned_data['address'],
                    longitude=long,
                    latitude=lat,
                    indoor=form.cleaned_data['indoor'],
                    contact_email=form.cleaned_data['contact_email'],
                    contact_phone=form.cleaned_data['contact_phone'],
                    image=_image
                )
       
                data.save()
                messages.success(request, 'Facility Added')
            else:
                messages.error(request, 'Failed to add Facility')
            return redirect('display_facilities')
        messages.error(request, 'No Access')
        return redirect('display_facilities')


# modify_facility
class modify_facility(LoginRequiredMixin, View):
    def get(self, request, facil_id):
        if (check_if_owned(request.user, facil_id) or
                request.user.is_superuser or
                check_group(request.user, "Admin")):

            data = bkm.Facility.objects.get(id=facil_id)
            form = bkf.FacilityForm(instance=data)
        else:
            return redirect('get_booking_index')
        return render(request, 'booking/facility/add_facility.html', {'form': form})

    def post(self, request, facil_id):
        if (check_if_owned(request.user, facil_id) or
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
                messages.success(request, 'Successfully modified Facility')
            else:
                messages.error(request, 'Failed to modify facility')
            return redirect('display_facilities')
        messages.error(request, 'No Access')
        return redirect('get_booking_index')


# modify_slots
class modify_timeslots(LoginRequiredMixin, View):

    def get(self, request, facil_id):
        if check_if_owned(request.user, facil_id) or check_group(request.user, "Admin"):

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

        return redirect('get_booking_index')

    def post(self, request, facil_id):
        if check_if_owned(request.user, facil_id) or check_group(request.user, "Admin"):

            if not request.POST.get('Data'):
                returned = []
            else:
                returned = request.POST.get('Data').split('|')
            
            data = []

            # Parse returned into a 2d list
            for r in returned:
                # remove the square brackets on each end of string                
                row = r[1:-1]
                row = row.split(',')
                if row[0] != "new":
                    row[0] = int(row[0])
                row[1] = parse_datetime("1999-11-23T"+row[1]+":00")
                row[2] = parse_datetime("1999-11-23T"+row[2]+":00")
                row[3] = True if row[3] == "true" else False
                row[4] = True if row[4] == "true" else False
                row[5] = True if row[5] == "true" else False
                row[6] = True if row[6] == "true" else False
                row[7] = True if row[7] == "true" else False
                row[8] = True if row[8] == "true" else False
                row[9] = True if row[9] == "true" else False
                data.append(row)

            current = bkm.TimeSlot.objects.filter(facility_id=facil_id)
            current_list = []
            for c in list(current):
                current_list.append(c.id)

            current_data = [d[0] for d in data if d[0] != "new"]

            # Remove each item that appears in both lists, remaining are to be removed from db
            remove = list(set(current_list) - set(current_data))

            for r in remove:
                bkm.TimeSlot.objects.filter(facility_id=facil_id, id=r).delete()

            # Add new timeslots, and update existing ones
            for d in data:
                bk = None

                # If start date is greater than end date dont make changes
                if d[1] > d[2]:
                    continue

                if d[0] == "new":
                    bk = bkm.TimeSlot()
                    bk.facility_id = bkm.Facility.objects.get(id=facil_id)

                else:
                    bk = bkm.TimeSlot.objects.get(id=int(d[0]))
                
                bk.start = d[1]
                bk.end = d[2]
                bk.monday = d[3]
                bk.tuesday = d[4]
                bk.wednesday = d[5]
                bk.thursday = d[6]
                bk.friday = d[7]
                bk.saturday = d[8]
                bk.sunday = d[9]
                bk.save()
            messages.success(request, 'Successfully modifed Time slots')
            return redirect('display_facilities')

        return redirect('get_booking_index')


# modify_facility_tags
class modify_facility_tags(LoginRequiredMixin, View):

    def get(self, request, facil_id):
        if check_if_owned(request.user, facil_id) or check_group(request.user, "Admin"):
            form_data = bkm.FacilityTag.objects.filter(facility_id=facil_id)
            tags = bkm.Tag.objects.all()

            info_tup = (facil_id, bkm.Facility.objects.get(id=facil_id).name)

            return render(request, 'booking/tag/modify_facility_tags.html', {'data': form_data, 'tags': tags, 'info_tup': info_tup})
        return redirect('get_booking_index')

    def post(self, request, facil_id):
        if check_if_owned(request.user, facil_id) or check_group(request.user, "Admin"):
            returned = request.POST.get('Data').split(',')
            returned = list(map(int, returned))

            # Get all tags currently in table for that facility
            current = bkm.FacilityTag.objects.filter(facility_id=facil_id)
            current_list = []
            for i in list(current):
                current_list.append(i.tag_id.id)

            # Get all id's that are not in the returned list
            remove = list(set([x for x in current_list if x not in returned]))

            # Get those that are not in current but are in returned
            #   turn to sets so that they can be subtracted from eachtother
            add = list(set(returned) - set(current_list))

            for r in remove:
                bkm.FacilityTag.objects.filter(facility_id=facil_id, tag_id=r).delete()

            for a in add:
                tg = bkm.Tag.objects.get(id=a)
                fac = bkm.Facility.objects.get(id=facil_id)
                new = bkm.FacilityTag(facility_id=fac, tag_id=tg)
                new.save()

            messages.success(request, 'Facility Tags Successfully Updated')
            return redirect('display_facilities')
        return redirect('get_booking_index')
#endregion


#region Booking
# make_booking
class view_times(LoginRequiredMixin, View):
    def get(self, request, facil_id):
        times = bkm.TimeSlot.objects.filter(facility_id=facil_id)
        bookings = bkm.Booking.objects.filter(facility_id=facil_id)

        # month as a int, 1 - 12
        def build_data(year, month):
            '''
            returns a 2d list containing: 
            Day: e.g. 1st, 2nd, 31st etc etc
            Day of week: Mainly for matching timeslots with the arrays in this function
            timeslots: a list of timeslot id's that fall on this day, followed by a bool
                to indicate if the time slot is currently take on that day
            '''

            calendar_rows = [month]
            month_data = calendar.monthrange(year, month)

            row = []

            for i in range(0, month_data[0]):
                row.append([0])

            day_of_week = 0
            day = 1
            for i in range(month_data[0], 7):
                day_of_week = i
                row.append([day, calendar.day_abbr[i], []])
                day += 1

            calendar_rows.append(row)
            row = []

            week_counter = 1
            while day != month_data[1]+1:
                row.append([day, calendar.day_abbr[week_counter-1], []])
                if week_counter == 7:
                    calendar_rows.append(row)
                    row = []
                    week_counter = 0
            
                week_counter += 1
                day += 1

            if row != []:
                calendar_rows.append(row)

            # Skip first value as it holds the month
            for cr in calendar_rows[1:]:
                for day in cr:
                    if day[0] == 0:
                        continue
                    if day[1] == "Mon":
                        day[2] = [[x, False] for x in times if x.monday]
                    elif day[1] == "Tue":
                        day[2] = [[x, False] for x in times if x.tuesday]
                    elif day[1] == "Wed":
                        day[2] = [[x, False] for x in times if x.wednesday]
                    elif day[1] == "Thu":
                        day[2] = [[x, False] for x in times if x.thursday]
                    elif day[1] == "Fri":
                        day[2] = [[x, False] for x in times if x.friday]
                    elif day[1] == "Sat":
                        day[2] = [[x, False] for x in times if x.saturday]
                    elif day[1] == "Sun":
                        day[2] = [[x, False] for x in times if x.sunday]

            found = False
            # Loop over each booking
            for b in bookings:
                # loop over each row of calendar
                for cr in calendar_rows[1:]:
                    if found:
                        found = False
                        break
                    # loop over each day
                    for day in cr:
                        # Check if days match
                        if day[0] == b.date.day and b.date.month == month:
                            # Find the index of the taken flag
                            dex = day[2].index([b.time_slot, False])
                            # Set the flag to true
                            day[2][dex][1] = True
                            # Indicate to outside flag to no longer loop
                            found = True
                            break

            return calendar_rows
        
        x = build_data(
            datetime.datetime.now().year,
            datetime.datetime.now().month)

        y = build_data(
            datetime.datetime.now().year,
            datetime.datetime.now().month + 1)

        form = bkf.BookingForm()
    
        return render(request, 'booking/book/view_times.html',
        {
            'current_month': x,
            'next_month': y,
            'form': form
        })

    def post(self, request, facil_id):
        form = bkf.BookingForm(request.POST)
        if form.is_valid():
            valid = True
            _facility = bkm.Facility.objects.get(id=facil_id)
            _timeslot = bkm.TimeSlot.objects.get(id=form.cleaned_data['timeslot'])
            _date = form.cleaned_data['date']

            exists = bkm.Booking.objects.filter(facility_id=_facility, time_slot=_timeslot, date=_date)

            if not exists.exists():
                day_of_week = calendar.day_abbr[_date.weekday()]
                if day_of_week == 'Mon':
                    if not _timeslot.monday:
                        valid = False
                elif day_of_week == 'Tue':
                    if not _timeslot.tuesday:
                        valid = False
                elif day_of_week == 'Wed':
                    if not _timeslot.wednesday:
                        valid = False
                elif day_of_week == 'Thu':
                    if not _timeslot.thursday:
                        valid = False
                elif day_of_week == 'Fri':
                    if not _timeslot.friday:
                        valid = False
                elif day_of_week == 'Sat':
                    if not _timeslot.saturday:
                        valid = False
                elif day_of_week == 'Sun':
                    if not _timeslot.sunday:
                        valid = False
                else:
                    valid = False

                if valid:
                    data = bkm.Booking(
                        facility_id=_facility,
                        time_slot=_timeslot,
                        user_id=request.user,
                        date=_date)
                    data.save()
                    messages.success(request, 'Booking Created!')
                    return redirect('list_bookings')
        return redirect('get_booking_index')


# list_facility_bookings
class list_facility_bookings(LoginRequiredMixin, View):
    def get(self, request, facil_id):
        if (check_if_super(request.user) or 
            check_group(request.user, "Admin") or 
            check_if_owned(request.user, facil_id)):

            bookings = bkm.Booking.objects.filter(facility_id=facil_id)

            return render(request, 'booking/book/view_bookings.html', {'bookings': bookings})
        messages.error(request, 'Access denied')
        return redirect('get_booking_index')


# list_bookings
class list_bookings(LoginRequiredMixin, View):
    def get(self, request, user_id=''):
        data = None
        if user_id != '':
            if check_if_super(request.user) or check_group(request.user, "Admin"):
                user = bkm.User.objects.filter(id=user_id)
                if user.exists():
                    data = bkm.Booking.objects.filter(user_id=user_id)
                else:
                    messages.error(request, "No matching user found")
        if not data:
            data = bkm.Booking.objects.filter(user_id=request.user.id)
        if not len(data):
            messages.error(request, 'No Bookings Found')
        return render(request, 'booking/book/user_bookings.html', {'bookings': data, 'form': bkf.SingleIdForm()})

    def post(self, request, user_id=''):
        if (check_if_super(request.user) or
            check_group(request.user, "Admin")):
            form = bkf.SingleIdForm(request.POST)
            if form.is_valid():
                if user_id != '':
                    # Checking user_id is probably not needed, but might aswell
                    data = bkm.Booking.objects.filter(id=form.cleaned_data['ID'], user_id=user_id)
                    if data.exists():
                        data.delete()
                        messages.success(request, 'Booking cancelled')
                else:
                    data = bkm.Booking.objects.filter(id=form.cleaned_data['ID'])
                    if data.exists():
                        data.delete()
                        messages.success(request, 'Booking cancelled')
        else:
            data = bkm.Booking.objects.filter(id=form.cleaned_data['ID'], user_id=request.user)
            if data.exists():
                data.delete()
                messages.success(request, 'Booking cancelled')
        return redirect('list_bookings')
#endregion
