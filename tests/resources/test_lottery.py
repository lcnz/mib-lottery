from flask import json
from .view_test import ViewTest
from faker import Faker


class TestLottery(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestLottery, cls).setUpClass()

    def test_retrieve_by_id(self):
        self.insert_test_lottery(50)
        