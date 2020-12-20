from __future__ import unicode_literals

from django.conf import settings
from django.apps import AppConfig
import beeline


HONEYCOMB_API_KEY=settings.HONEYCOMB_API_KEY

class ConfabulationConfig(AppConfig):
    name = 'confabulation'
    def ready(self):
        # If you use uwsgi, gunicorn, celery, or other pre-fork models, see the section below on pre-fork
        # models and do not initialize here.
            beeline.init(
                writekey=HONEYCOMB_API_KEY,
                dataset='confabulations-v3',
                service_name='confabulations-v3',
                #debug=True,
            )
