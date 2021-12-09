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
    sender.add_periodic_task(crontab(hour=12, minute = 0, day_of_month=27), lottery.s(), name = 'lottery extraction')

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

        winner = random.randrange(1,100)#exctract a random number in [1,99]
        
        players = LotteryManager.retrieve_active_players()     #users who play the lottery
        if not players:
            return []
        for p in players:
            if p.ticket_number == winner:      # if player's number is the extracted number, then he wins
                p.add_points(5)                   #winner user gains 5 points
            p.unset_ticket_number()        #restore default value for every player at the end of lottery extraction
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