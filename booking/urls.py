from django.urls import path
import booking.views as bkv

urlpatterns = [
    path('', bkv.get_booking_index, name='get_booking_index'),
    path('logout/', bkv.logout_view, name='logout_view'),
    path('login/', bkv.login_view.as_view(), name='login_view'),
    path('register/', bkv.register_view.as_view(), name='register'),
    path('tags/', bkv.list_tags, name='list_tags'),
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
        bkv.make_booking.as_view(),
        name='view_booking'
    ),
    path(
        'map_test',
        bkv.get_map_test,
        name='map_test'
    ),
    path(
        'search/<int:sport_tag>/<str:location_search_area>/<int:radius>',
        bkv.search_facilities,
        name='search_facilities'
    )
]
