# Bookit
A website for booking the use of and making postings for sports facilities.

## User Stories
- As a user I want to be able to create an account
- As a user I want to be able to search for a facility by tag, location and radius
- As a user I want to make a booking at a facility of my chouce
- As a user I want to be able to see all of my bookings
- As a facility owner I want to be able to make multiple new facilities
- As a facility owner I want to edit my pre-existing facilities
- As a facility owner I want to be able edit my facilities
- As a facility owner I want to be able to add new timeslots to my facilities
- As a facility owner I want to be able to modify my existing facilities timeslots
- As a facility owner I want to be able to delete existing timeslots
- As a facility owner I want to add new tags to my facilities
- As a facility owner I want to remove tags from my facilities
- As a admin I want to be able to create new tags
- As a admin I want to be able to modify existing tags
- As a admin I want to be able to be able to delete existing tags
- As a admin I want to be able to make changes

## UX
As the site revolves around a single purpose I chose to keep the UX simple and have multiple ways to this main purpose,(which is booking a sports facility) at a time, so that the user is always able to get to the search page.

For the actual booking page, I will be using a calendar and a table, from which the user will select a date from the calendar and the table will be updated to display a list times. This will be an easy to understand and use system, while also being easy to display on both mobile and desktop devices.

All admin/owner pages will be table layouts as they will be mainly just displaying data and this will be the easiest and most concise way to display such data.

### Color Scheme
I will be using only two colors for the site, Blue, #1d71b8 and Green, #44ad47. 

### Typography
Gill Sans. I do not feel multiple are needed for a simple site.

### Wireframes
Register

Login

Search
![](documentation/index.png)

Results
![](documentation/search_results.png)

Book
![](documentation/time_slots.png)

View Bookings
![](documentation/list_bookings.png)

View Facilities

Modify Timeslots
![](documentation/modify_timeslots.png)

Modify Facility Tags
![](documentation/facility_tags.png)

## Features
### Existing Features
- Nav bar leading to differnt pages
![](documentation/screenshots/header.png)
- Search form on index

- A list of sports offered
    - Taken from the "Tag" table and updates live to reflect the table
    - (Take again without placeholders)
    ![](documentation/screenshots/sports_cards.png)

- Clickable calendar to visually choose what date you want
    - Reveals a table of times available on that date
    - Booked times will still be shown by greyed out
    ![](documentation/screenshots/booking_page.png)

- Page to see all of your bookings
    - With the functionality to cancel it
    ![](documentation/screenshots/my_bookings.png)

- Form to search for facilities
    - Takes a tag via drop down
    - A location (preferably a town)
    - A distance in miles
    ![](documentation/screenshots/search_form.png)

- A Search results page that lists relevant facilities and has a form to make another search
    - Each card will have the facility image and its location
    ![](documentation/screenshots/search_results.png)

#### Admin Features
- See all the facilities you are in charge of
    - Or if site Admin see all facilities
    ![](documentation/screenshots/admin_facilities.png)

- Edit the tags of a facility
    ![](documentation/screenshots/admin_facility_tags.png)

- Edit, Add, Remove sports to tag facilities with (Site admins only)
    ![](documentation/screenshots/admin_tags.png)

- Edit, Add and Remove timeslots from facilities
    ![](documentation/screenshots/admin_timeslots.png)












### Features left to implent
- Use googles geocode api as its more precise (currently it is paid for)
- Have a clickable map for facility owners to select where there facility it
- Results page will have a form on it
- Admins/Facility owners able to cancel bookings
- Email updates to users when booked or cancelled
- Upload related image to Tag to display it on front page
- Show available days on results screen

## Technologies used
- I used [git](https://git-scm.com/) for version control and storage.
- To help with using git, I used [github](https://github.com/).

- I used [html](https://en.wikipedia.org/wiki/HTML) to design the site.
- And [CSS](https://en.wikipedia.org/wiki/CSS) to style the site.
- For most of the sites layout ive used [Bootstrap](https://getbootstrap.com/) and its many [examples](https://getbootstrap.com/docs/5.2/examples/) to help with quick development
- Using [Django](https://www.djangoproject.com/) to create the backend to the site
- For some of the forms like "facility/tags/modify/", and the calendar on the booking page I used [Javascript](https://en.wikipedia.org/wiki/JavaScript) and [JQuery](https://jquery.com/) to create the functionality
- To help with styling I used a css debugger to help me with things like positioning and size: [link](https://github.com/benscabbia/x-ray).
- For my IDE I used Gitpod, [link](https://www.gitpod.io/).
- To host static files like images and css i used [Cloudinary](https://cloudinary.com/) and its django library "cloudinary"
- To deploy the website I used [Heroku](https://dashboard.heroku.com/)