from flask_restful import Resource, Api
from flask import Flask, request
from base64 import b64decode
import uuid
import logging
import os
from pathlib import Path

logging.basicConfig(level=logging.DEBUG, filename=os.path.dirname(os.path.realpath(__file__)) + '/debug.log')

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'status': 'success, this is the media understanding API'}


class Image(Resource):
    def post(self):
        # Decode received image
        json_data = request.get_json()
        image_encoded = json_data['image']
        image = b64decode(image_encoded)

        # Save incoming image to unique file name
        image_id = str(uuid.uuid1())
        file = 'images/' + image_id + '.jpg'
        with open(file, 'wb') as f:
            logging.debug('Writing file as {}'.format(file))
            f.write(image)

        # Check if image is saved
        path = Path(file)
        if not path.exists():
            logging.debug('Saving the image file seems to have failed')
            return {'status': 'failed, image does not seem to be saved'}, 500

        # TODO run neural net

        # Cleanup
        os.remove(file)

        response_success = {
            'status': 'success',
            'imageId': image_id,
            'plantName': 'not set',
            'description': 'plant description'
        }

        return response_success, 200


api.add_resource(HelloWorld, '/')
api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run(debug=True)
