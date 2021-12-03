#from mib import create_app, create_celery
#
#flask_app = create_app()
#app = create_celery(flask_app)
#
#try:
#    import mib.tasks
#except ImportError:
#    raise RuntimeError('Cannot import celery tasks')
from datetime import date, datetime, timedelta
from celery import Celery
from celery.schedules import crontab
import random 
from smtplib import SMTPRecipientsRefused

BACKEND = BROKER = 'redis://lottery_ms_redis:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

celery.conf.timezone = 'Europe/Rome'
_APP = None

@celery.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=12, minute = 0, day_of_month=27), lottery.s(), name = 'lottery extraction')

# task fo the lottery
@celery.task
def lottery():
    global _APP
    # lazy init
    if _APP is None:
        from mib import create_app
        
        from sqlalchemy import update

        app = create_app()
        mail = Mail(app)
        db.init_app(app)
        with app.app_context():
            winner = random.randrange(1,100)#exctract a random number in [1,99]
            players = db.session.query(User).filter(User.lottery_ticket_number != -1)     #users who play the lottery
            for p in players:
                if p.lottery_ticket_number == winner:      # if player's number is the extracted number, then he wins
                    p.set_points(5)                   #winner user gains 5 points
                    
                    """Background task to send an email with Flask-Mail."""
                    
                    subject = "Monthly Lottery Result"
                    body = "you have earned 5 points"
                    to_email = p.email
                    receiver_id = p.id
                    
                    email_data = {
                        'subject': subject,
                        'to': to_email,
                        'body': body
                    }
                    msg = Message(email_data['subject'], sender=app.config['MAIL_DEFAULT_SENDER'],recipients=[email_data['to']])
                    msg.body = email_data['body']
                    mail.send(msg)
                p.set_lottery_number(-1)        #restore default value for every player at the end of lottery extraction
            db.session.commit()  
            return []  
    else:
        app = _APP
    return []
   