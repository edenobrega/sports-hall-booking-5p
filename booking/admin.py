from django.contrib import admin
from .models import Facility, Tag, FacilityTag, TimeSlot, Booking

# Register your models here.
admin.site.register(Facility)
admin.site.register(Tag)
admin.site.register(FacilityTag)
admin.site.register(TimeSlot)
admin.site.register(Booking)
