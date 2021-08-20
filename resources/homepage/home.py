from flask_restful import Resource
from flask import redirect


class Home(Resource):
    @classmethod
    def get(cls):
        # return redirect('/', 301)
        return {'msg': 'Welcome to PrinterConnect.'}, 200
