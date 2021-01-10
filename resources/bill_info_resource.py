from flask_jwt_extended import jwt_required
from flask_restful import Resource, reqparse

from models.bill_info_model import BillsInfoModel

parser = reqparse.RequestParser()
parser.add_argument('car_id', help='This field cannot be blank', required=True)
parser.add_argument('expire')
parser.add_argument('amount')


class BillRegistration(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        return BillsInfoModel.save(data)
