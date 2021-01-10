from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.driver_model import DriverModel, driver_to_json

parser = reqparse.RequestParser()
parser.add_argument('first_name', help='This field cannot be blank', required=True)
parser.add_argument('last_name', help='This field cannot be blank', required=True)
parser.add_argument('email')
parser.add_argument('phone')


class DriverRegistration(Resource):
    # @jwt_required
    def post(self):
        data = parser.parse_args()
        new_driver = DriverModel(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data['phone']
        )
        try:
            new_driver.save_to_db()
            return {
                "message": f"new driver added : {data['first_name']}  {data['last_name']}"
            }
        except Exception as e:
            print(e)
            return {'message': f"Something went wrong - {e}"}, 500


class AllDriver(Resource):
    @jwt_required
    def get(self):
        return DriverModel.return_all()
    @jwt_required
    def delete(self):
        return DriverModel.delete_all()


class SingleDriver(Resource):
    @jwt_required
    def get(self, id):
        driver = DriverModel.get_by_id(id)
        if driver:
            return {"driver": driver_to_json(driver)}
        else:
            return {"message": f"driver by id : {id} not found"}

    @jwt_required
    def delete(self, id):
        return DriverModel.delete_by_id(id)

    @jwt_required
    def put(self, id):
        data = parser.parse_args()
        return DriverModel.update_driver_by_id(id, data)
