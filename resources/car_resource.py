from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.car_model import CarModel, car_to_json

parser = reqparse.RequestParser()
parser.add_argument('name', help='This field cannot be blank', required=True)
parser.add_argument('phone_number', help='This field cannot be blank', required=True)
parser.add_argument('gas_car')
parser.add_argument('status')


class CarRegistration(Resource):
    # @jwt_required
    def post(self):
        data = parser.parse_args()
        new_car = CarModel(
            name=data['name'],
            phone_number=data['phone_number'],
            gas_car=bool(data['gas_car']),
            status=data['status']
        )
        try:
            new_car.save_to_db()
            return {
                "message": f"new car added : {data['name']} - {data['phone_number']}"
            }
        except Exception as e:
            print(e)
            return {'message': f"Something went wrong - {e}"}, 500


class AllCar(Resource):
    @jwt_required
    def get(self):
        return CarModel.return_all()

    @jwt_required
    def delete(self):
        return CarModel.delete_all()


class SingleCar(Resource):
    @jwt_required
    def get(self, id):
        car = CarModel.get_by_id(id)
        if car:
            return {"car": car_to_json(car)}
        else:
            return {"message": f"car by id : {id} not found."}

    @jwt_required
    def delete(self, id):
        return CarModel.delete_by_id(id)

    @jwt_required
    def put(self, id):
        data = parser.parse_args()
        return CarModel.update_by_id(id, data)
