Return to [README](README.md)

# Testing
## User Accounts
- When trying to login to an account that doesnt exist or with incorrect details the error message is shown
![](documentation/testing/incorrect_no_exist.png)
- Once logged in the navbar will change
![](documentation/testing/login_change_nav.png)
- Must fill all required inputs to create an account
![](documentation/testing/failed_signup.png)

## Search
- Searching for facilities will return the correct amount within the given radius
![](documentation/testing/successful_search_step1.png)
![](documentation/testing/successful_search_step2.png)

- Searching an area with no facilities will return none with a message saying so
![](documentation/testing/unsuccessful_search_step1.png)
![](documentation/testing/unsuccessful_search_step2.png)

## Bookings
- Nav link will lead to a page showing you all of your bookings
![](documentation/testing/view_my_bookings.png)
- Viewing a day with a booked timeslot will be in grey with no booking button
![](documentation/testing/booked.png)
- Selecting a day and clicking book will give a pop up before booking
![](documentation/testing/booking.png)
- Cancelling a booking will delete it and display the relevant message
![](documentation/testing/cancel.png)
- As an admin can see all bookings for a facility, and cancel them
![](documentation/testing/bookings_others.png)
![](documentation/testing/cancel_other.png)

## Tags
- Can view all tags
![](documentation/screenshots/admin_tags.png)
- Can modify tags
![](documentation/testing/modify_admin_tag.png)
- Can delete tags
![](documentation/testing/tag_delete_message.png)
![](documentation/testing/success_delete_tag.png)
- Can create tags
![](documentation/testing/tag_create_form.png)
![](documentation/testing/tag_create_success.png)

## Facilities
- Can View facilities
![](documentation/screenshots/admin_facilities.png)
- Can Create facility
![](documentation/CRUD/facility_delete.png])
- Can Delete facility
![](documentation/testing/delete_facility.png)
![](documentation/testing/delete_success.png)
- Can Modify Facility
![](documentation/CRUD/facility_modify.png)
- Can Modify Facility Tags
![](documentation/CRUD/facility_tags_modify_delete_add.png)
- Can Modify Facility Time Slots
![](documentation/CRUD/timeslots_whole_crud.png) 

# Responsiveness
Screenshots taken on mobile for the two pages that a user who is booking would see
- Index
![](documentation/testing/index_mobile.png)
- Search Result
![](documentation/testing/search_result_mobile.png)

# Code Validation
- PEP8 validation for view.py, giving no errors or warnings
![](documentation/view_py.png)