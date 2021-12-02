from flask import request, jsonify
from mib.dao.lottery_manager import LotteryManager
from mib.models.lottery import Lottery
from datetime import datetime as dt

def retrieve_by_id(id):
    user = LotteryManager.retrieve_by_id(id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200 


# Creating the row for the user in the database (called when a user register himself)
def lottery_create_user(id):
    #check if the id is already present in the database
    user = LotteryManager.retrieve_by_id(id)
    if user is not None:
        response = {'status': 'User already present'}
        return jsonify(response), 409

    #new row for lottery
    lottery = Lottery()
    lottery.set_id(id)
    lottery.set_points(0)
    lottery.unset_ticket_number()
    
    #adding the row to the database
    user = LotteryManager.create_lottery(lottery)
    
    #DEBUG
    print("THE NEW ROW HAS BEEN CREATED")
    print("THE ID JUST ADDED IS ", id)
    print("TRYING TO RETRIEVE THE ROW ---> ", retrieve_by_id(id))