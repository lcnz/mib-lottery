from sqlalchemy.orm import relationship
from mib import db

class Lottery(db.Model):
    __tablename__ = 'Lottery'
    SERIALIZE_LIST = ['id', 'ticket_number', 'points']

    id = db.Column(db.Integer, primary_key=True)
    ticket_number = db.Column(db.Integer, default = -1) #lottery ticker number 0-99
    points = db.Column(db.Integer, default = 0) #points gained with the monthly lottery

    def __init__(self, *args, **kw):
        super(Lottery, self).__init__(*args, **kw)

    def set_ticket_number(self, number):
        self.ticket_number = number

    def unset_ticket_number(self):
        self.ticket_number = -1

    def set_points(self, points):
        self.points = points

    def serialize(self):
        return dict([(k,self.__getattribute__(k)) for k in self.SERIALIZE_LIST])
