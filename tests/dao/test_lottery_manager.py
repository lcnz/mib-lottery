from faker import Faker

from .dao_test import DaoTest
from  tests.models.test_lottery import TestLottery
from random import randrange


class TestLotteryManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestLotteryManager, cls).setUpClass()
        from tests.models.test_lottery import TestLottery
        cls.test_lottery = TestLottery
        from mib.dao import lottery_manager
        cls.lottery_manager = lottery_manager.LotteryManager

    def test_crlot(self):
        for _ in range(0, 10):
            lottery = self.test_lottery.generate_random_lottery_row()
            self.lottery_manager.create_lottery(lottery=lottery)
            lottery1 = self.lottery_manager.retrieve_by_id(lottery.id)
            self.test_lottery.assertLotteryEquals(lottery1, lottery)
            lottery.set_ticket_number(randrange(100))
            self.lottery_manager.update_lottery_row(lottery=lottery)
            lottery1 = self.lottery_manager.retrieve_by_id(lottery.id)
            self.test_lottery.assertLotteryEquals(lottery1, lottery)

        self.lottery_manager.retrieve_active_players() 
        