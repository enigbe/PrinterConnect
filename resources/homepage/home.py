from flask_restful import Resource


class Home(Resource):
    @classmethod
    def get(cls):
        return {'msg': 'Welcome to PrinterConnect.'}, 200
