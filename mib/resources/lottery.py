from flask import request, jsonify
from mib.dao.lottery_manager import LotteryManager
from datetime import datetime as dt

def retrieve_by_id(id):
    user = LotteryManager.retrieve_by_id(id)
    if user is None:
        response = {'status': 'User not present'}
        return jsonify(response), 404

    return jsonify(user.serialize()), 200 