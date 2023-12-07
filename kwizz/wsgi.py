"""
WSGI config for kwizz project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import django
django.setup()

import os


from django.core.wsgi import get_wsgi_application
import socketio
from host.views import sio
import eventlet
import eventlet.wsgi
from django.contrib.staticfiles.handlers import StaticFilesHandler

django_app = StaticFilesHandler(get_wsgi_application())

application = socketio.Middleware(sio, wsgi_app=django_app, socketio_path='socket.io')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kwizz.settings')

# application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)

serverIP = "localhost"
# serverIP = "192.168.208.29"
# serverIP = "192.168.208.145"

# eventlet.wsgi.server(eventlet.listen((serverIP, 8000)), application)