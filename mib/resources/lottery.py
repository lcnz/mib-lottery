from flask import request, jsonify
from mib.dao.lottery_manager import LotteryManager
from mib.models.lottery import Lottery
from datetime import datetime as dt


def retrieve_by_id(id):
    lottery_row = LotteryManager.retrieve_by_id(id)
    if lottery_row is None:
        response = {'status': 'Id of user not present'}
        return jsonify(response), 404
    response = {'status': 'success', 'lottery_row': lottery_row.serialize()}
    return jsonify(response), 200 


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
    
    return {'status': 'success', 'about': 'lottery_user created'}, 201



def select_number(id):
    lottery_row = LotteryManager.retrieve_by_id(id)
    if lottery_row is None:
        response = {'status': 'Id of user not present'}
        return jsonify(response), 404

    #selecting the number
    selected_number = request.get_json().get('val_')
    lottery_row.set_ticket_number(selected_number)
    LotteryManager.update_lottery_row(lottery_row)

    return {'status': 'success', 'about': 'lottery number selected'}, 201


def update_lottery_points():
    user_id = request.get_json().get('userid')
    val = request.get_json().get('value')

    lottery_row = LotteryManager.retrieve_by_id(user_id)
    if lottery_row is None:
        response = {'message': 'error'}
        return jsonify(response), 404
    else:
        LotteryManager.update_lottery_points(user_id, val)
        response = {'message':'success'}
        return response, 200