import logging
import os
import uuid
from base64 import b64decode
from pathlib import Path
import json

from flask import Flask, request
from flask_restful import Resource, Api

import torch
from cnn.pytorch_main import single_prediction
from cnn.pytorch_main import used_classes

from time import gmtime, strftime

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)


class HelloWorld(Resource):
    def get(self):
        return {'status': 'success, this is the media understanding API'}


class Image(Resource):
    def post(self):
        plant_info = json.load(open('data/plant_info.json', mode='r'))

        # Decode received image
        json_data = request.get_json()
        image_encoded = json_data['image']
        image = b64decode(image_encoded)

        # Save incoming image to unique file name
        image_id = str(uuid.uuid1())
        time = strftime("%Y_%m_%d_%H_%M_%S", gmtime())
        file = 'images/' + time + '_' + image_id + '.jpg'
        with open(file, 'wb') as f:
            logging.debug('Writing file as {}'.format(file))
            f.write(image)

        # Check if image is saved
        path = Path(file)
        if not path.exists():
            logging.debug('Saving the image file seems to have failed')
            return {'status': 'failed, image does not seem to be saved'}, 500

        _, name_predicted = single_prediction(str(path), used_classes())
        response_success = plant_info['plantInfo'][name_predicted]

        # Cleanup
        # os.remove(file)

        return response_success, 200


api.add_resource(HelloWorld, '/')
api.add_resource(Image, '/image')

if __name__ == '__main__':
    app.run(debug=True)
