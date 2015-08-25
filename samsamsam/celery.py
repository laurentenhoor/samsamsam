from __future__ import absolute_import

from celery import Celery
from kombu import serialization
serialization.registry._decoders.pop("application/x-python-serialize")

app = Celery('samsamsam',
             broker='amqp://',
             backend='amqp://',
             include=['paypal.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    CELERY_TASK_RESULT_EXPIRES=3600,
)

if __name__ == '__main__':
    app.start()