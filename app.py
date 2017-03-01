from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'This is the media understanding API'}

class Image(Resource):
    def post(self):

        return {'status': 'success'}, 200

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)