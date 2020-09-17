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
First, checkout 'develop' branch.

~~~bash
$ git checkout develop
~~~

Go to the directory which has manage.py.
Then, run this command:

~~~bash
$ python manage.py runserver
~~~

and open http://127.0.0.1:8000/make/ in your favorite browser.

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/682620/02531d08-446c-97cf-262f-40e6f798bf1b.png)

Upload a excel file that includes all infomation of classes and choose the number of classes for each day.
Then, push the blue button and you will go to http://127.0.0.1:8000/make/constraint/ like below.

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/682620/f0d54002-e8f5-9ab6-c303-b4fc49ac8e8d.png)

Then, add conveniences of teachers and choose the machine which you have access token for. Decide the number od steps and the number of loops, and push the blue button. You will go to http://127.0.0.1:8000/make/success/. Here are some candidates of timetable.

![image.png](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/682620/a27ed0ea-8351-5a0a-2a74-c14311d8ec12.png)
