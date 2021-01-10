import datetime

from sqlalchemy import DateTime

from models.car_model import CarModel
from models.driver_model import DriverModel
from run import db


class TimeTableModel(db.Model):
    __timetable__ = 'timetable'
    id = db.Column(db.Integer, primary_key=True)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id', ondelete="cascade"))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id', ondelete="cascade"))
    car = db.relationship("CarModel", uselist=False)
    driver = db.relationship("DriverModel", uselist=False)
    used_at = db.Column(DateTime)
    used_time = db.Column(DateTime)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def new_timetable(cls, data):
        driver_id = data['driver_id']
        car_id = data['car_id']
        car = CarModel.get_by_id(car_id)
        driver = DriverModel.get_by_id(driver_id)
        if car and driver:
            new_timetable = TimeTableModel(
                car=car,
                driver=driver,
                used_time=datetime.datetime.strptime(data['used_time'], '%y/%m/%d'),
                used_at=datetime.datetime.strptime(data['used_at'], '%y/%m/%d')
            )
            new_timetable.save_to_db()
            return {"message": f"save timetable to db by id : {new_timetable.id}"}
        else:
            return {"message": "wrong data for car or driver"}
