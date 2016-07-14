import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from recommender import Recommender


app = Flask(__name__)
auth = HTTPBasicAuth()
recommender = Recommender()
env = os.environ.get('APP_ENV')
if env:
    app.config.from_object('config.' + env)
else:
    app.config.from_object('config.Development')
db = SQLAlchemy(app)


@auth.verify_password
def verify_password(username, password):
    if username == app.config['BEEHIVE_INSIGHT_TOKEN'] and password == app.config['BEEHIVE_INSIGHT_SECRET']:
        return True


@app.route('/', methods=['GET'])
@auth.login_required
def root():
    return 'Signed in as Admin'


@app.route('/update', methods=['GET'])
@auth.login_required
def update():
    recommender.save_funders_data()
    from models import FunderBeneficiary
    records = []
    for record in FunderBeneficiary.query.order_by(FunderBeneficiary.fund_slug).all():
        records.append(record.serialize)
    return render_template('update.html', records=records)


@app.route('/beneficiaries', methods=['POST'])
@auth.login_required
def beneficiaries():
    data = request.json['data']
    result = recommender.recommend_funders(data)
    return jsonify(result)


if __name__ == "__main__":
    app.run()
