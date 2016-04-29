import os
from flask import Flask, jsonify, request
from flask.ext.httpauth import HTTPBasicAuth
from recommender import Recommender


app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    if username == os.environ['ADMIN_TOKEN']:
        return True

@app.route('/', methods=['POST'])
def root():
    data = request.json['recipient']
    return jsonify({'r': data})

@app.route('/recommend', methods=['POST'])
@auth.login_required
def recommend():
    data = request.json['data']
    result = Recommender.recommend_funders(2014, data)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
