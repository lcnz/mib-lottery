import unittest

from faker import Faker

from .model_test import ModelTest
from random import randrange

class TestLottery(ModelTest):

    faker = Faker()

    @classmethod
    def setUpClass(cls):
        super(TestLottery, cls).setUpClass()

        from mib.models import lottery
        cls.lottery = lottery

    @staticmethod
    def assertLotteryEquals(value, expected):
        t = unittest.FunctionTestCase(TestLottery)
        t.assertEqual(value.id, expected.id)
        t.assertEqual(value.ticket_number, expected.ticket_number)
        t.assertEqual(value.points, expected.points)
        
    @staticmethod
    def generate_random_lottery_row():
        id = randrange(100)
        ticket_number = randrange(100)
        points = 0

        from mib.models import Lottery

        lottery = Lottery(
            id = id,
            ticket_number = ticket_number,
            points = points
        )

        return lottery

    def test_set_ticket_number(self):
        row = TestLottery.generate_random_lottery_row()
        row.set_ticket_number(15)

        self.assertEqual(
            row.ticket_number,
            15
        )
    def test_unset_ticket_number(self):
        row = TestLottery.generate_random_lottery_row()
        row.unset_ticket_number()
        self.assertEqual(
            row.ticket_number,
            -1
        )
    def test_add_points(self):
        row = TestLottery.generate_random_lottery_row()
        points = row.points
        row.add_points(5)
        self.assertEqual(row.points, points+5)

    def test_set_points(self):
        row = TestLottery.generate_random_lottery_row()
        row.set_points(5)
        self.assertEqual(row.points,5)
