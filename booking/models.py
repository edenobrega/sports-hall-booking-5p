from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Facility(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    address = models.CharField(max_length=200)
    indoor = models.BooleanField()
    contact_email = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    image = CloudinaryField('image', default='placeholder')


class Tag(models.Model):
    shorthand = models.CharField(max_length=50)
    description = models.CharField(max_length=300)


class FacilityTag(models.Model):
    facility_id = models.ForeignKey(Facility(), on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)


class TimeSlot(models.Model):
    facility_id = models.ForeignKey(Facility, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    monday = models.BooleanField()
    tuesday = models.BooleanField()
    wednesday = models.BooleanField()
    thursday = models.BooleanField()
    friday = models.BooleanField()
    saturday = models.BooleanField()
    sunday = models.BooleanField()


class Booking(models.Model):
    facility_id = models.ForeignKey(Facility, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
