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
## Python
- Validation for view.py, giving no errors or warnings
![](documentation/view_py.png)
- Validation for forms.py
![](documentation/testing/forms.png)
- Validation for group_check.py
![](documentation/testing/group_check.png)
- Validation for month_name.py
![](documentation/testing/month_name.png)
- Validation for ordinal_format.png
![](documentation/testing/ordinal_format.png)
- Validation for models.py
![](documentation/testing/models.png)
- Validation for urls.py 
![](documentation/testing/urls.png)

## HTML
Validated using https://validator.w3.org
- [Index](https://validator.w3.org/nu/?doc=https%3A%2F%2Fbookit-5p.herokuapp.com)
- [Login](https://validator.w3.org/nu/?doc=https://bookit-5p.herokuapp.com/login)
- [Register](https://validator.w3.org/nu/?doc=https://bookit-5p.herokuapp.com/register)

- view_times.html
![](documentation/testing/make_booking.png)

- search_results.html
![](documentation/testing/search_results.png)

- view_bookings
![](documentation/testing/view_facility_bookings.png)

- modify_timeslots
![](documentation/testing/modify_timeslots.png)

- modify_facility_tags
![](documentation/testing/modify_facility_tags.png)

- modify_facility
![](documentation/testing/modify_facility.png)


## CSS
For css I have used https://jigsaw.w3.org/css-validator to validate my stylesheets
- [calender.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653754742%2Fstatic%2Fcss%2Fcalender.ba4248a0e6d9.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [edit_tags.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1651229170%2Fstatic%2Fcss%2Fedit_tags.ca532f4f9149.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [index.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653569905%2Fstatic%2Fcss%2Findex.88d033533e16.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [list_facility.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653868144%2Fstatic%2Fcss%2Flist_facility.1d04c4500c10.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [list_tags.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653868144%2Fstatic%2Fcss%2Flist_tags.8994ac72288d.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [login.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653564284%2Fstatic%2Fcss%2Flogin.b0671f9ed80e.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [modal.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653569904%2Fstatic%2Fcss%2Fmodal.ad6eb2a34f31.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [modify_facility_tags.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653564284%2Fstatic%2Fcss%2Fmodify_facility_tags.243e84a9bbb7.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [modify_timeslots.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653564283%2Fstatic%2Fcss%2Fmodify_timeslots.ea40933244ba.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [Search_results.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653868144%2Fstatic%2Fcss%2Fsearch_results.73235d1e58a0.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
- [style.css](https://jigsaw.w3.org/css-validator/validator?uri=https%3A%2F%2Fres.cloudinary.com%2Fdcjvfcg2q%2Fraw%2Fupload%2Fv1653564282%2Fstatic%2Fcss%2Fstyle.c73d8f77d3d4.css&profile=css3svg&usermedium=all&warning=1&vextwarning=&lang=en)
