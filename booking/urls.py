from django.urls import path
import booking.views as bkv

urlpatterns = [
    path('', bkv.index_view.as_view(), name='get_booking_index'),
    path('logout/', bkv.logout_view, name='logout_view'),
    path('login/', bkv.login_view.as_view(), name='login_view'),
    path('register/', bkv.register_view.as_view(), name='register'),
    path('tags/', bkv.list_tags.as_view(), name='list_tags'),
    path('tags/<int:tag_id>', bkv.edit_tag.as_view(), name='edit_tag'),
    path('tags/create', bkv.create_tag.as_view(), name='create_tag'),
    path(
        'facility/create',
        bkv.create_facility.as_view(),
        name='create_facility'),
    path('facility/', bkv.display_facility, name='display_facilities'),
    path(
        'facility/tags/modify/<int:facil_id>',
        bkv.modify_facility_tags.as_view(),
        name='modify_facility_tags'),
    path(
        'facility/modify/<int:facil_id>',
        bkv.modify_facility.as_view(),
        name='modify_facility'),
    path(
        'facility/times/modify/<int:facil_id>',
        bkv.modify_timeslots.as_view(),
        name='modify_slots'),
    path(
        'facility/book/<int:facil_id>',
        bkv.view_times.as_view(),
        name='make_booking'
    ),
    path(
        'facility/book/list/<int:facil_id>',
        bkv.list_facility_bookings.as_view(),
        name='list_facility_bookings'
    ),
    path(
        'user/bookings/<int:user_id>',
        bkv.list_bookings.as_view(),
        name='list_bookings_id'
    ),
    path(
        'user/bookings',
        bkv.list_bookings.as_view(),
        name='list_bookings'
    ),
    # path(
    #     'tags/delete/<int:tag_id>'
    # ),
]
