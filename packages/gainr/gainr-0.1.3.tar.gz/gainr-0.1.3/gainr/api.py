from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse, abort

from gainr.dac81416 import SetGain

APP = Flask(__name__)
API = Api(APP)


parser = reqparse.RequestParser()
parser.add_argument("channels", type=dict)


class Channels(Resource):
    def post(self):
        args = parser.parse_args()
        channels = args["channels"]

        not_set = set(range(8))
        for channel in channels:
            not_set.remove(int(channel))
        if not_set:
            print(not_set)
            not_set_str = " ".join([str(i) for i in sorted(not_set)])
            abort(400, message=f"All 8 channels must be defined. Those are not defined: {not_set_str}")

        channels_list = list()
        for i in range(8):
            channels_list.append(channels[str(i)])

        message = SetGain(channels_list)
        return jsonify({"message": message})

API.add_resource(Channels, '/api/channels')
