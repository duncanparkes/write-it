You write it, and we deliver it.
================================

[![Build Status](https://travis-ci.org/ciudadanointeligente/write-it.png?branch=master)](https://travis-ci.org/ciudadanointeligente/write-it)
[![Coverage Status](https://coveralls.io/repos/ciudadanointeligente/write-it/badge.png?branch=master)](https://coveralls.io/r/ciudadanointeligente/write-it)
[![Code Health](https://landscape.io/github/ciudadanointeligente/write-it/master/landscape.png)](https://landscape.io/github/ciudadanointeligente/write-it/master)

Write-it is an application that aims to deliver messages to people whose contacts are to be private or the messages should be public, for example: members of congress. 

Write-it is a layer on top of [popit](http://popit.mysociety.org) from where it takes the people and adds contacts. The way it delivers messages is using plugins for example: mailit. And this approach allows for future ways of delivering for example: twitter, whatsapp, fax or pager.

Future uses are in [votainteligente](http://www.votainteligente.cl) to replace the old "preguntales" (You can [check here](http://municipales2012.votainteligente.cl/valdivia/preguntales), to see how it used to work) feature, could be in the way for the site [writetothem](http://www.writetothem.com/) and any parliamentary monitoring site.



Installation
------------

System Requirements
-------------------

 * [Elasticsearch](http://www.elasticsearch.org/)

 It's required if you want to play around seaching messages and answers, this part is optional.

 * [Urllib3](http://urllib3.readthedocs.org/en/latest/)

 * [libffi](https://sourceware.org/libffi/)

 In ubuntu you can do ```sudo apt-get install libffi-dev```

 * Libssl

 In ubuntu you can do ```sudo apt-get install libssl-dev```



Write-it is built using Django. You should install Django and its dependencies inside a virtualenv. We suggest you use [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/) to create and manage virtualenvs, so if you don’t already have it, [go install it](http://virtualenvwrapper.readthedocs.org/en/latest/install.html#basic-installation), remembering in particular to add the required lines to your shell startup file.

With virtualenvwrapper installed, clone this repo, `cd` into it, and create a virtualenv:

    git clone git@github.com:ciudadanointeligente/write-it.git
    cd write-it
    mkvirtualenv writeit

Install the requirements:

    pip install -r requirements.txt

Set up the database, creating an admin user when prompted:

    ./manage.py syncdb && ./manage.py migrate

Troubleshooting database migration
----------------------------------
There's a problem migrating and the problem looks like 

	django.db.utils.OperationalError: no such table: tastypie_apikey

It can be fixed by running it twice.

Then run the server:

    ./manage.py runserver




Testing and Development
-----------------------

If you want to test without PopitAPI or Elasticsearch
-----------------------------------------------------
Elasticsearch and a popit api both are optional and can be turned off by creating a new local_settings.py file ```vi writeit/local_settings.py``` with the following content


```
LOCAL_POPIT = False
LOCAL_ELASTICSEARCH = False
```

Testing with Popit and Elasticsearch
------------------------------------
If you want to test the pulling from popit parts, we're using a separate popit-api from which to pull people. For that you need to have MongoDB running, here is the [download page and installation instructions](http://www.mongodb.org/downloads).

After you have mongodb running you can do in a separate terminal:

	./start_local_popit_api.bash

Running tests
--------------

For testing you need to run ```./test.py```

Coverage Analysis
-----------------
For coverage analysis run ./coverage.sh


API clients
-----------

Write-it has been used mostly through its REST API for which there are a number of API clients.
The github repos and the status of the development are listed below:
- [writeit-rails](https://github.com/ciudadanointeligente/writeit-rails) ALPHA
- [writeit-django](https://github.com/ciudadanointeligente/writeit-django) ALPHA


There are instructions to install write-it in heroku
----------------------------------------------------
The instructions are in [the following link](deploying_to_heroku.md).
