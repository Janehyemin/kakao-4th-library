from flask import Flask
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)


class HealthCehck(Resource):
    def get(self):
        return {'message': 'alive'}

    def post(self):
        self.get()


api.add_resource(HealthCehck, '/', '/health_check')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()

