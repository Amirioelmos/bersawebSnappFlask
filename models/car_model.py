from run import db
from enum import Enum, unique
from sqlalchemy.dialects.postgresql import ENUM as pgEnum


@unique
class CarStatus(Enum):
    good_condition = 'good_condition'
    bad_condition = 'bad_condition'


def car_to_json(x):
    return {
        'id': x.id,
        'name': x.name,
        'phone_number': x.phone_number,
        'gas_car': x.gas_car,
        'status': str(x.status),
    }


class CarModel(db.Model):
    __tablename__ = 'car'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(11), nullable=False)
    gas_car = db.Column(db.Boolean)
    status = db.Column(pgEnum(CarStatus))

    bills = db.relationship("BillsInfoModel", backref='car', lazy='dynamic')
    drivers = db.relationship("TimeTableModel")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        return {'cars': list(map(lambda x: car_to_json(x), CarModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} car row(s) deleted'.format(num_rows_deleted)}
        except:
            return {'message': 'Something went wrong'}

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.query.filter_by(id=id).first()
        except:
            return 0

    @classmethod
    def delete_by_id(cls, id):
        try:
            _ = db.session.query(cls).filter_by(id=id).delete()
            db.session.commit()
            return {"message": f"delete car by id: {id}"}
        except Exception as e:
            return {"message": f"error in delete car {e}"}

    @classmethod
    def update_by_id(cls, id, data):
        try:
            update_car_dict = {
                "name": data['name'],
                "phone_number": data['phone_number'],
                "gas_car": bool(data['gas_car']),
                "status": str(data['status'])}
            db.session.query(cls) \
                .filter_by(id=id) \
                .update(update_car_dict)
            db.session.commit()
            return {"message": f"updated car by id : {id} to {update_car_dict}"}
        except Exception as e:
            return {"message": f"fail to update car by id : {id} - error : {e}"}
