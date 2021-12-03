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
from celery.signals import worker_ready
import random 
from smtplib import SMTPRecipientsRefused
from mib import create_app
BACKEND = BROKER = 'redis://lottery_ms_redis:6379'
celery = Celery(__name__, backend=BACKEND, broker=BROKER)

celery.conf.timezone = 'Europe/Rome'
APP = None

@celery.on_after_configure.connect
def setup_periodic_task(sender, **kwargs):
    #sender.add_periodic_task(crontab(hour=12, minute = 0, day_of_month=27), lottery.s(), name = 'lottery extraction')
    sender.add_periodic_task(timedelta(seconds = 60), lottery.s(), name = 'lottery extraction')

# task fo the lottery
@celery.task
def lottery():
    global APP
    # lazy init
    if not APP :
        return 
    with APP.app_context():
        from mib import create_app
        from mib.dao.lottery_manager import LotteryManager
        #from sqlalchemy import update

        winner = random.randrange(1,100)#exctract a random number in [1,99]
        print("lucky number -----", winner)
        players = LotteryManager.retrieve_active_players()     #users who play the lottery
        if not players:
            return []
        for p in players:
            print(loooooop)
            #LotteryManager.check_winner(p) #
            if p.lottery_ticket_number == winner:      # if player's number is the extracted number, then he wins
                p.add_points(5)                   #winner user gains 5 points
                
                """Background task to send an email with Flask-Mail."""
                
                """subject = "Monthly Lottery Result"
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
                mail.send(msg)"""
            p.unset_ticket_number()        #restore default value for every player at the end of lottery extraction
            print()
        LotteryManager.update_lottery_row(p)  
        return []  
    

@worker_ready.connect
def init(sender, **k):
    with sender.app.connection() as c:
        sender.app.send_task('background.initialization', connection = c)

@celery.task
def initialization():
    global APP
    if APP is None:
        APP = create_app()
    else:
        app = APP
    return []