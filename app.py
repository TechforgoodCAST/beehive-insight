import os
from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from recommender import Recommender
from fund_request import FundRequest


app = Flask(__name__)
auth = HTTPBasicAuth()
env = os.environ.get('APP_ENV')
if env:
    app.config.from_object('config.' + env)
else:
    app.config.from_object('config.Development')
db = SQLAlchemy(app)

recommender = Recommender()
fund_request = FundRequest()


@auth.verify_password
def verify_password(username, password):
    if username == app.config['BEEHIVE_INSIGHT_TOKEN'] and password == app.config['BEEHIVE_INSIGHT_SECRET']:
        return True


@app.route('/', methods=['GET'])
@auth.login_required
def root():
    return 'Signed in as Admin'


@app.route('/update_beneficiaries', methods=['GET'])
@auth.login_required
def update():
    # TODO: refacor
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
    return render_template(
        'update_amounts.html',
        records=fund_request.save_fund_amounts()
    )


@app.route('/check_amount', methods=['POST'])
@auth.login_required
def check_amount():
    data = request.json['data']['amount']
    result = fund_request.check_amount(data)
    return jsonify(result)


@app.route('/update_durations', methods=['GET'])
@auth.login_required
def update_durations():
    return render_template(
        'update_durations.html',
        records=fund_request.save_fund_durations()
    )


@app.route('/check_duration', methods=['POST'])
@auth.login_required
def check_duration():
    data = request.json['data']['duration']
    result = fund_request.check_duration(data)
    return jsonify(result)

if __name__ == "__main__":
    app.run()
