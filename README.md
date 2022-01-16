# django-polling_site

> forked from https://github.com/aahnik/django-polling-site
>
> **BE AWARE THAT THERE IS A DEFAULT SUPERUSER CREATED ON THE ORIGINAL PROJECT**

django-polling_site ( Life's First Django Project)

[![GitHub license](https://img.shields.io/github/license/aahnik/django-polling_site)](https://github.com/aahnik/django-polling_site/blob/master/LICENSE)
[![No Maintenance Intended | Archived](http://unmaintained.tech/badge.svg)](https://gitHub.com/aahnik/django-polling_site/graphs/commit-activity)


[**see screenshots**](https://github.com/aahnik/django-polling_site/tree/master/ScreenShots)

## Project state

 * [ ] `channels` branch
         * https://channels.readthedocs.io/en/latest/tutorial/part_2.html
         * [ ] front : showWait()
         * [ ] WC and results synchros
         * [ ] back : sync notificaton from admin 
         * [ ] back : admin widget for handling question order
         * rewrite code as async if needed
 * [ ] TUTO deployment & customization
 * [ ] home as django models (for non-technical people)
 * [ ] docker wrapping
 * [ ] django app wrapping
 * [ ] FR translation


## How to run on your computer

__pre-requisites : python(3.8 or above) and pip must be installed__ 



**1. create and activate a virtual environment inside a new directory**

if you are new to virtual environments read [python-3 official docs](https://docs.python.org/3/library/venv.html) 

**2. clone this repo `django-polling-site` in your directory, and install the requirements**

```
pip install -r requirements.txt
```

**3. move inside the `pollsite` directory and make migrationS**

```
python manage.py makemigrations home
python manage.py makemigrations poll
python manage.py migrate
```

**4. create a superuser , with your own username and password**

```
python manage.py createsuperuser
```

**5. Collect Static files needed**

```
python manage.py collectstatic
```

**6. Inside the `home` app directory , configure the homePage.yaml according to your wish**
Inside `views.py` of same directory, put the absolute path of homePage.yaml in the place instructed. 

**7. now run the server**

```
python manage.py runserver
```

Go to  http://127.0.0.1:8000/ . This is where Django starts server by default

**HOLA !! ENJOY YOU HAVE SUCCESSFULLY RUN THE SERVER**

Click on Admin button on top right corner to go the the Django Administration page.
You can add team members , change or add questions and choices


*Vist DJANGO'S OFFICIAL WEBSITE FOR MORE DETAILS..*

__you can now play around with the code your self__

