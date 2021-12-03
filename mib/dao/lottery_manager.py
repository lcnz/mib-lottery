from mib.dao.manager import Manager
from mib.models.lottery import Lottery
from sqlalchemy import update
from mib import db

class LotteryManager(Manager):

    @staticmethod
    def create_lottery(lottery: Lottery):
        Manager.create(lottery=lottery)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Lottery.query.get(id_)

    @staticmethod
    def retrieve_active_players():
        return Lottery.query.filter(Lottery.ticket_number != -1)
    @staticmethod
    def create_row(lottery: Lottery):
        Manager.create(lottery=lottery)
        
    @staticmethod
    def update_lottery_row(lottery: Lottery):
        Manager.update(lottery=lottery)

    @staticmethod
    def check_winner()