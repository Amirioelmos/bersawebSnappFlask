from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://snapp:ljhsdlkjfhsdf@localhost:5432/snapp_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'some-secret-string'

db = SQLAlchemy(app)


@app.before_first_request
def create_tables():
    db.create_all()


app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    from models.revoked_token_model import RevokedTokenModel
    return RevokedTokenModel.is_jti_blacklisted(jti)


from resources import user_resource, car_resource, driver_resource, bill_info_resource, timetable_resource

# user
api.add_resource(user_resource.UserRegistration, '/registration')
api.add_resource(user_resource.UserLogin, '/login')
api.add_resource(user_resource.UserLogoutAccess, '/logout/access')
api.add_resource(user_resource.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_resource.AllUsers, '/users')

# car
api.add_resource(car_resource.CarRegistration, '/car/register')
api.add_resource(car_resource.AllCar, '/car/all')
api.add_resource(car_resource.SingleCar, '/car/<id>')

# driver
api.add_resource(driver_resource.DriverRegistration, '/driver/register')
api.add_resource(driver_resource.AllDriver, '/driver/all')
api.add_resource(driver_resource.SingleDriver, '/driver/<id>')

# bills
api.add_resource(bill_info_resource.BillRegistration, '/bill/')

# timetable
api.add_resource(timetable_resource.DriverUsedCar, '/timetable/')
