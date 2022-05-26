from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Published"))


class Facility(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=8)
    address = models.CharField(max_length=200)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    indoor = models.BooleanField()
    contact_email = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    image = CloudinaryField('image', default='placeholder')

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    shorthand = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    image = CloudinaryField('image', default='https://res.cloudinary.com/dcjvfcg2q/image/upload/v1653561731/placeholder_hm2nkw.png')

    def __str__(self):
        return f"{self.shorthand}"


class FacilityTag(models.Model):
    facility_id = models.ForeignKey(Facility(), on_delete=models.CASCADE)
    tag_id = models.ForeignKey(Tag, on_delete=models.CASCADE)


    def __str__(self):
        return f"fid:{self.facility_id} tid:{self.tag_id}"


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

    def __str__(self):
        return f"fid:{self.facility_id} start:{self.start} end:{self.end}"


class Booking(models.Model):
    facility_id = models.ForeignKey(Facility, on_delete=models.CASCADE)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return (f"fid:{self.facility_id} uid:{self.user_id} "
                f"time:{self.time_slot} date:{self.date}")
