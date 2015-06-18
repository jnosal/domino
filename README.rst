Manual
------------

Useful settings (location domino/settings/base.py)
IMAGE_CONTENT_TYPES - acceptable image content types
IMAGE_COLOR_PERSIST_MODE - whether hex or color name should be taken into consideration when constructing color set
IMAGE_EXTRACTION_MODE - whether color extraction should run in 'sync' or 'async' mode


1. Clone project

.. code-block:: bash

    $ git clone git@github.com:jnosal/domino.git .

2. Install virtualenv

.. code-block:: bash

    $ virtualenv venv/ && source venv/bin/activate

3. Install requirements

.. code-block:: bash

    $ pip install -r requirements.txt

4. If You'll be using async mode install rabbitmq

.. code-block:: bash

    $ sudo apt-get install rabbitmq-server
    $ sudo service rabbitmq-server start

5. Create database (it creates sqlite3 database && applies migrations)

.. code-block:: bash

    $ python manage.py recreate_db

6. Run tests

.. code-block:: bash

    $ ./scripts/runtests.sh


7. Run project (by default sync extraction mode and name persist mode)

.. code-block:: bash

    $ python manage.py runserver


8. Post couple of files

.. code-block:: bash

    $ curl -X POST -F "image1=@data/cobra.jpg" -F "image2=@data/onlywhite.jpg" http://localhost:8000/api/v1/imagefile


9. Explore

.. code-block:: bash

    $ curl -X GET http://localhost:8000/api/v1/imagefile/search\?format\=json


10. Search for color

.. code-block:: bash

    $ curl -X GET http://localhost:8000/api/v1/imagefile/search\?format\=json\&color\=crimson


11. Search for hex

.. code-block:: bash

    $ curl -X GET http://localhost:8000/api/v1/imagefile/search\?format\=json\&hex\=fcfcfc

12. Run in assync mode

    a) edit domino/settings/base.py and replace IMAGE_EXTRACTION_MODE = 'sync' with IMAGE_EXTRACTION_MODE = 'async'
    b) this assumes that rabbitmq is installed & running


Stop & start application again (after editing settings)


.. code-block:: bash

    $ python manage.py runserver


In other terminbal start Celery worker


.. code-block:: bash

    $ celery -A domino worker --loglevel=INFO


Image handling should be significantly faster:

.. code-block:: bash

    $ curl -X POST -F "image1=@data/cobra.jpg" -F "image2=@data/onlywhite.jpg" http://localhost:8000/api/v1/imagefile