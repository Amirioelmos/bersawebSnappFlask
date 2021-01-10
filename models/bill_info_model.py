import datetime

from sqlalchemy import DateTime

from models.car_model import CarModel
from run import db


class BillsInfoModel(db.Model):
    __tablename__ = 'bills_info'

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(DateTime, default=datetime.datetime.utcnow)
    amount = db.Column(db.Integer)
    expire = db.Column(DateTime)

    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def save(cls, data):
        try:
            car_id = data['car_id']
            car = CarModel.get_by_id(car_id)
            new_bill = BillsInfoModel(
                expire=datetime.datetime.strptime(data['expire'], '%y/%m/%d'),
                amount=data['amount']
            )
            car.bills.append(new_bill)
            car.save_to_db()
            return {"message": f"add new bill to car by id : {car_id}"}

        except Exception as e:
            return {"message": f"fail to add bill : {e}"}
