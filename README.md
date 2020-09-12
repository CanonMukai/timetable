# TIMETABLE for School
This is a Web Application to make a timetable for high schools or junior high schools in Japan. It's developped by python web application frame work 'Django'.

This application solve the Scheduling problem by quantum annealing or simulated annealing (SA). If you have a access token for D-Wave, Digital Annealer, or anything else, you can make some timetables for your school by using an annealing machine. You don't have one? That's okay. You can solve the problem by SA.  

## Install django
Run the command:

~~~bash
$ pip install django
~~~

## How to install this app
There are 2 ways to install.
* Download a zip file and decompress it.
* Use a command ```git clone``` like below:

~~~bash
$ git clone https://github.com/CanonMukai/timetable/
~~~

## How to run
Go to the directory which has manage.py.
Then, run this command:

~~~bash
$ python manage.py runserver
~~~

and open http://127.0.0.1:8000/make/ in your favorite browser.