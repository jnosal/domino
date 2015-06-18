#!/bin/bash

LOCATION=$(pwd)

DJANGO_SETTINGS_MODULE="domino.settings.tests" $LOCATION/venv/bin/python $LOCATION/manage.py test -p tests --verbosity=2 $1 --settings="domino.settings.tests"