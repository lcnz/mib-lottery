from faker import Faker

from .dao_test import DaoTest
from  tests.models.test_lottery import TestLottery


class TestLotteryManager(DaoTest):
    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestLotteryManager, cls).setUpClass()
        from tests.models.test_lottery import TestLottery
        cls.test_lottery = TestLottery
        from mib.dao import lottery_manager
        cls.lottery_manager = lottery_manager.LotteryManager

    def test_crud(self):#A CHE SERVE?
        for _ in range(0, 10):
            row = self.test_lottery.generate_random_lottery_row()
            self.user_manager.create_user(user=user)
            user1 = self.user_manager.retrieve_by_id(user.id)
            self.test_user.assertUserEquals(user1, user)
            user.set_password(self.faker.password())
            user.email = self.faker.email()
            self.user_manager.update_user(user=user)
            user1 = self.user_manager.retrieve_by_id(user.id)
            self.test_user.assertUserEquals(user1, user)
            self.user_manager.delete_user(user=user)

    def test_retried_by_email(self):
        base_user = self.test_user.generate_random_user()
        self.user_manager.create_user(user=base_user)
        retrieved_user = self.user_manager.retrieve_by_email(email=base_user.email)
        self.test_user.assertUserEquals(base_user, retrieved_user)
