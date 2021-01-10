from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.timetable_model import TimeTableModel

parser = reqparse.RequestParser()
parser.add_argument('car_id')
parser.add_argument('driver_id')
parser.add_argument('used_at')
parser.add_argument('used_time')


class DriverUsedCar(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        return TimeTableModel.new_timetable(data)
