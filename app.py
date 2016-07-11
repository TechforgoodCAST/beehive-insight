import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from recommender import Recommender


app = Flask(__name__)
auth = HTTPBasicAuth()
recommender = Recommender()
app.config.from_object(os.environ.get('APP_ENV') or 'config.DevelopmentConfig')
db = SQLAlchemy(app)


@auth.verify_password
def verify_password(username, password):
    if username == os.environ.get('ADMIN_TOKEN'):
        return True


@app.route('/', methods=['GET'])
@auth.login_required
def root():
    return 'Success!'


@app.route('/recommend', methods=['POST'])
@auth.login_required
def recommend():
    data = request.json['data']
    result = recommender.recommend_funders(data)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
