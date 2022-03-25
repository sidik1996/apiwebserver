from flask import Flask, request, make_response, jsonify
from flask_restful import Resource, Api
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
import jwt
import os
import datetime

app = Flask(__name__)
api = Api(app)
db = SQLAlchemy(app)
CORS(app)

filename = os.path.dirname(os.path.abspath(__file__))
database = 'sqlite:///' + os.path.join(filename, 'sidikdwiayu.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database
app.config['SECRET_KEY'] = 'sidik123'

class AuthModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
db.create_all()

class Registerpengguna(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        if dataUsername and dataPassword:
            dataModel = AuthModel(username=dataUsername, password=dataPassword)
            db.session.add(dataModel)
            db.session.commit()
            return make_response(jsonify({"Msg ":"Berhasil Register"}), 200)
        return jsonify({"Msg ":"Username/Password tidak boleh KOSONG"})

class Loginpengguna(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            
            return make_response(jsonify({"Selamat Datang " : dataUsername}), 200)
        return jsonify({"Msg ":"Login Gagal, Coba Lagi"}) 

class infopengguna(Resource):
    def post(self):
        dataUsername = request.form.get('username')
        dataPassword = request.form.get('password')

        queryUsername = [data.username for data in AuthModel.query.all()]
        queryPassword = [data.password for data in AuthModel.query.all()]
        if dataUsername in queryUsername and dataPassword in queryPassword:
            token = jwt.encode(
                {
                    "username":queryUsername, 
                    "exp":datetime.datetime.utcnow() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'], algorithm="HS256"
            )
            return make_response(jsonify({"Username": dataUsername,"Password": dataPassword,"Token API":token}), 200)
        return jsonify({"Msg ":"Gagal Mengambil Info"}) 

api.add_resource(Registerpengguna, "/api/v1/register", methods=["POST"])
api.add_resource(Loginpengguna, "/api/v1/login", methods=["POST"])
api.add_resource(infopengguna, "/api/v2/users/info", methods=["POST"])

if __name__ == "__main__":
    app.run(port=4000, debug=True)