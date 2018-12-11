import _thread

from flask import Flask, jsonify
from flask import request

# config of restful-api
app = Flask(__name__)

# note: 1 - wolny/odblokowany , 2 - zajety samochod, 3 - zarezerowwany
parking = [
    {"id": 0,
     "type": 1},

    {"id": 1,
     "type": 1}
]


@app.route('/', methods=['GET'])
def api_root():
    if request.method == 'GET':
        return jsonify(parking)



@app.route('/block/<id>', methods=['GET'])
def api_block(id):
    print(id)
    return jsonify(parking)


@app.route('/unblock/<id>', methods=['GET'])
def api_unblock(id):
    print('super idddd')
    print(type(id))
    for spot in parking:
        if (int(id) == spot['id']):
            spot['type'] = 100000
            print('done')
    return jsonify(parking)


def serverStart():
    app.run()

# main Loop

if __name__ == '__main__':
    app.run()
