from __future__ import absolute_import

from celery import shared_task


@shared_task
def sendEmails(emails):
    connection = mail.get_connection()
    # Manually open the connection
    connection.open()
    
    # Send the two emails in a single call -
    connection.send_messages(emails)
    # The connection was already open so send_messages() doesn't close it.
    # We need to manually close the connection.
    connection.close()
    return ''


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)