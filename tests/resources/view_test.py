import unittest


class ViewTest(unittest.TestCase):
    """
    This class should be implemented by
    all classes that tests resources
    """
    client = None

    @classmethod
    def setUpClass(cls):
        from mib import create_app
        app = create_app()
        cls.client = app.test_client()
        from tests.models.test_lottery import TestLottery
        cls.test_lottery = TestLottery
        from mib.dao.lottery_manager import LotteryManager
        cls.lottery_manager = LotteryManager()
        
    
    def insert_test_lottery(self, id_):
        """
        Insert a fake row in the lottery table
        :return: user
        """
        response = self.lottery_manager.create_lottery_row(id = id_)
        print("RESPONSEEE")
        print(response)
        json_response = response.json
        return json_response
