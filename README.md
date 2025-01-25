# Hotel Website With Booking System
## Video Demo:  [This is the project video](https://youtu.be/JH-JP-CGnu0)
#### Description: My project is about a website for a hotel that allows users to book a room.

### What is my project is about?
This is my final project in CS50x and this website is for a hotel where users can book a room, the first time the user visits the website he will see a home page with a hero image and below it, there is a form that the user will include his check-in date and check-out date and the number of people with him and the number of rooms the user wants after the user clicks _search_, it will send to the rooms page where the user can see the available rooms after that the user can book the desired room. I used HTML, CSS, Bootstrap, and some JavaScript for the website's front end, I chose my primary language Python, and the Flask framework for the back end.

### What do each of my files are, contain and do?
My main files for the project are _app.py_, _bookings.db_, and a folder called _templates_ which contains HTML files, what each of them contains: _app.py_ contains my main Python code which handles the logic of the website and also queries the database for the website.

The database file _bookings.db_ also contains 4 tables _booked_rooms_ table which stores when the user books a room _reservations_ table which stores the check-in and check-out date of the user and the _rooms_ table which stores the room information Standard room, Deluxe room, Suite and _users_ tables which also stores the user’s information.

The folder _templates_ contain HTML files and the main ones are _index.html_ which is the home page and _rooms.html_ which is the page that displays the room information and _reservations.html_ which will show the user his reservation information which includes check-in and check-out date and the number of people with him and the number of rooms that the user wants and _about.html_ which shows some important information about the hotel and _login.html_ and _register.html_ which registers and logins the user and _gallery.html_ which shows the slideshows of some images of the hotel.

When the user is not logged in to the website the user will see a few pages which are the home page, about page, register page, and login page, and he can’t search a room if he enters the check-in and check-out date, if he does that and clicks _search_ when he enters his information there is will be an error message telling the user to login first. Also when the user login to the website or registers as a new user he will be allowed to see all the pages.

### Why did I choose this design for the website?
The design of my website consists of the main color Caribbean green and the hex is _#00cc99_.
The background mostly is _White_. The font of my website is _Raleway_. I chose this design because is elegant in my eyes and hopefully, I would be glad if this design appeals to others as well.

The design chosen was a little bit different from that firstly, the font I was not planning to make it _Raleway_ font, I first decided on a font more like _Roboto_ because it has more flexibility than other fonts and I was also thinking about _Open Sans_. Finally, I chose _Raleway_ because I liked it more.

The color I wanted was more like red for the main color and decided to make it Caribbean green lastly, I chose this color because it looked more appealing to me, and the website look and pages could get more similar and beautiful if I chose this design.

### Conclusion
First I will thank Allah for allowing me to complete this course. Alhamdulillah, I will thank all CS50x staff for this great course and prof David for his energetic teaching, without this course I would not have been able to build this website and this was the first programming course I took, and I can say now I am in a place to build what I always wanted to build, right now my project lacks many functionalities and as my skills improve in the next weeks I will try to improve this project farther and again thank you, Harvard, for this great course.
