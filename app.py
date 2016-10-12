import os
from flask import Flask, json, jsonify, request, render_template
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
    return render_template('home.html')


@app.route('/new-beneficiary', methods=['GET'])
@auth.login_required
def new_beneficiary():
    return render_template('new_beneficiary.html')


@app.route('/create-beneficiary', methods=['POST'])
@auth.login_required
def create_beneficiary():
    # TODO: refactor
    if len(request.form['fund_slug']) < 1:
        raise ValueError('fund_slug too short')

    from models import FunderBeneficiary  # TODO:
    recommender.get_or_create(
        db.session, FunderBeneficiary,
        request.form['fund_slug'],
        json.loads(request.form['data']),
        True
    )
    return jsonify(request.form)


@app.route('/edit-beneficiary/<fund_slug>', methods=['GET'])
@auth.login_required
def edit_beneficiary(fund_slug):
    from models import FunderBeneficiary  # TODO:
    record = db.session.query(FunderBeneficiary).filter_by(fund_slug=fund_slug).first()
    data = {k: v for (k, v) in record.serialize.items() if 'fund_slug' not in k}
    data = json.dumps(record.serialize, ensure_ascii=False)
    return render_template('edit_beneficiary.html', record=record, data=data)


@app.route('/delete-beneficiary/<fund_slug>', methods=['GET'])
@auth.login_required
def delete_beneficiary(fund_slug):
    from models import FunderBeneficiary  # TODO:
    record = db.session.query(FunderBeneficiary).filter_by(fund_slug=fund_slug).first()
    db.session.delete(record)
    db.session.commit()
    return fund_slug + ' deleted'


@app.route('/update-beneficiary', methods=['POST'])
@auth.login_required
def update_beneficiary():
    # TODO: refactor
    if len(request.form['fund_slug']) < 1:
        raise ValueError('fund_slug too short')

    from models import FunderBeneficiary  # TODO:
    recommender.get_or_create(
        db.session, FunderBeneficiary,
        request.form['fund_slug'],
        json.loads(request.form['data']),
        request.form['manual']
    )
    return jsonify(request.form)


@app.route('/update-beneficiaries', methods=['GET'])
@auth.login_required
def update_beneficiaries():
    # TODO: refacor
    from models import FunderBeneficiary
    recommender.save_funders_data()
    records = []
    for record in FunderBeneficiary.query.order_by(FunderBeneficiary.fund_slug).all():
        records.append(record.serialize)
    return render_template('update_beneficiaries.html', records=records)


@app.route('/beneficiaries', methods=['POST'])
@auth.login_required
def beneficiaries():
    data = request.json['data']
    result = recommender.recommend_funders(data)
    return jsonify(result)


@app.route('/update-amounts', methods=['GET'])
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


@app.route('/update-durations', methods=['GET'])
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
