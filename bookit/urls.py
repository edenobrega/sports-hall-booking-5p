"""bookit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import booking.views as bkv
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', bkv.get_booking_index, name='get_booking_index'),
    path('logout/', bkv.logout_view, name='logout_view'),
    path('login/', bkv.login_view.as_view(), name='login_view'),
    path('register/', bkv.register_view.as_view(), name='register'),
    path('tags/', bkv.list_tags, name='list_tags'),
    path('tags/<int:tag_id>', bkv.edit_tag.as_view(), name='edit_tag'),
    path('tags/create', bkv.create_tag.as_view(), name='create_tag')
]
