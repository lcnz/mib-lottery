from flask import json
from .view_test import ViewTest
from faker import Faker


class TestLottery(ViewTest):
    faker = Faker('it_IT')

    @classmethod
    def setUpClass(cls):
        super(TestLottery, cls).setUpClass()

    #create a new row for the user
    def test_lottery(self):
        resp = self.client.post('/lottery/555')
        assert resp.status_code == 201
        
        #create again the same user
        resp = self.client.post('/lottery/555')
        assert resp.status_code == 409
        
        #select a number 
        resp = self.client.post('/lottery/select_number/555', json = {'val_': 23})
        assert resp.status_code == 201
        
        #select number on non-existing usr
        resp = self.client.post('/lottery/select_number/-1' , json = {'val_': 23})
        assert resp.status_code == 404
        
        #updating lottery points fo a user
        resp = self.client.post('/lottery/update_points', json = {'userid': 555, 'value': 88})
        assert resp.status_code == 200
        
        #updating lottery points for a non-existing user
        resp = self.client.post('/lottery/update_points', json = {'userid': -1, 'value': 88})
        assert resp.status_code == 404
        
        
      
        
        

