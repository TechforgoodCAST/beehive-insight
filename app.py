import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from recommender import Recommender
from amount import Amount


app = Flask(__name__)
auth = HTTPBasicAuth()
recommender = Recommender()
amount = Amount()
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
    from models import FunderBeneficiary
    recommender.save_funders_data()
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


@app.route('/update_amounts', methods=['GET'])
@auth.login_required
def update_amounts():
    from models import FundAmount
    amount.save_fund_amounts()
    records = []
    for record in FundAmount.query.order_by(FundAmount.fund_slug).all():
        records.append(record.serialize)
    return render_template('update_amounts.html', records=records)


@app.route('/check_amount', methods=['POST'])
@auth.login_required
def check_amount():
    data = request.json['data']['amount']
    result = amount.check_amount(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
