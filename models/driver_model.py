from models.car_model import CarModel
from run import db


def driver_to_json(x):
    return {
        'id': x.id,
        'first_name': x.first_name,
        'last_name': x.last_name,
        'email': x.email,
        'phone': x.phone,
    }


class DriverModel(db.Model):
    __tablename__ = "driver"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20))
    phone = db.Column(db.String(11))

    cars = db.relationship("TimeTableModel")

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def return_all(cls):
        return {'driver': list(map(lambda x: driver_to_json(x), DriverModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} driver row(s) deleted'.format(num_rows_deleted)}
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
            return {"message": f"delete driver by id: {id}"}
        except Exception as e:
            return {"message": f"error in delete driver {e}"}

    @classmethod
    def update_driver_by_id(cls, id, data):
        try:
            update_driver_dict = {
                "first_name": data['first_name'],
                "last_name": data['last_name'],
                "email": data['email'],
                "phone": data['phone']}
            db.session.query(cls) \
                .filter_by(id=id) \
                .update(update_driver_dict)
            db.session.commit()
            return {"message": f"updated driver by id : {id} to {update_driver_dict}"}
        except Exception as e:
            return {"message": f"fail to update driver by id : {id} - error : {e}"}


