from flask import Flask, jsonify
from flask import request
from flask_cors import CORS, cross_origin

# config of restful-api
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# note: 1 - wolny/odblokowany , 2 - zajety samochod, 3 - zarezerowwany
parking = [
    {"id": 0,
     "type": 1},

    {"id": 1,
     "type": 1}
]


@app.route('/', methods=['GET'])
@cross_origin()
def api_root():
    if request.method == 'GET':
        return jsonify(parking)



@app.route('/block/<id>', methods=['GET'])
@cross_origin()
def api_block(id):
    for spot in parking:
        if (int(id) == spot['id']):
            spot['type'] = 3
    return jsonify(parking)


@app.route('/unblock/<id>', methods=['GET'])
@cross_origin()
def api_unblock(id):
    for spot in parking:
        if (int(id) == spot['id']):
            spot['type'] = 1
    return jsonify(parking)


def serverStart():
    app.run()

# main Loop

if __name__ == '__main__':
    app.run()
