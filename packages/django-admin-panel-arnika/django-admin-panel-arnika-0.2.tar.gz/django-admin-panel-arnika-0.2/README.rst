django-admin-panel-arnika est un modèle pour Django Manager

This admin panel has been edited by jazzmin and works only for the right languages


Quick start
-----------

1. Add to terminal:

.. code-block:: bash

   pip install django-admin-panel-arnika

2. Add jazzmin to the first list before admin app:

.. code-block:: bash

    INSTALLED_APPS = [
        'jazzmin',

    ]

3. change in settings.py:

.. code-block:: bash

   LANGUAGE_CODE = 'fa-ir'

4. add to urls.py:

.. code-block:: python

   from django.urls import include
   from jazzmin.view import register
   urlpatterns = [
       path("i18n/", include("django.conf.urls.i18n")),
       path("", include("django.contrib.auth.urls")),
       path('register', register, name='register'), ]
   ]


5.run to server
