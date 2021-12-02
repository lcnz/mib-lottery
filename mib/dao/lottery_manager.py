from mib.dao.manager import Manager
from mib.models.lottery import Lottery
from sqlalchemy import update
from mib import db

class LotteryManager(Manager)

    @staticmethod
    def create_user(lottery: Lottery):
        Manager.create(lottery=lottery)

    @staticmethod
    def retrieve_by_id(id_):
        Manager.check_none(id=id_)
        return Lottery.query.get(id_)