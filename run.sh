#!/bin/bash

gunicorn --bind :4444 wsgi:app --preload