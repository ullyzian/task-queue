from app import celery, app, mail
from flask_mail import Message
import time


@celery.task(bind=True)
def send_async_email(self, email_data):
    msg = Message(subject=email_data['subject'],
                  sender=app.config["MAIL_DEFAULT_SENDER"],
                  recipients=[email_data['to']],
                  body=email_data['body'])
    with app.app_context():
        mail.send(msg)
    
    for i in range(0, 100, 1):
        self.update_state(state="PROGRESS", meta={'current': i, 'total': 100, 'status': 'Sending'})
        time.sleep(0.03)

    return {'current': 100, 'total': 100, 'status': 'Sent to ' + email_data['to']}