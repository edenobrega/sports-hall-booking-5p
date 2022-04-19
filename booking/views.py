from django.shortcuts import render
from django.views import generic

# Create your views here.

def get_booking_index(request):
    return render(request, 'booking/index.html')
