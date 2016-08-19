import os
import requests
import pandas as pd
import scipy.stats


class Amount:

    def __init__(self):
        import config
        env = os.environ.get('APP_ENV') or 'Development'
        self.config = getattr(config, env)

    def read_json(self):
        url = self.config.BEEHIVE_DATA_AMOUNT_ENDPOINT
        token = self.config.BEEHIVE_DATA_TOKEN
        headers = {'Authorization': 'Token token=' + token}
        response = requests.get(url, headers=headers)
        df = pd.read_json(response.text)
        df.set_index('fund_slug', inplace=True)
        return df

    def save_fund_amounts(self):
        from app import db
        from models import FundAmount
        df = self.read_json()
        dic = df.to_dict(orient='index')
        for item in dic.items():
            self.get_or_create(db.session, FundAmount, item[0], item[1])

    # TODO: refactor
    def get_or_create(self, session, model, slug, data):
        instance = session.query(model).filter_by(fund_slug=slug).first()
        if instance:
            instance.update(data)
            session.commit()
            return instance
        else:
            instance = model(slug, data['amounts'])
            session.add(instance)
            session.commit()
            return instance

    def check_amount(self, request_amount):
        from models import FundAmount

        result = {}
        tolerance = 10000
        min_request = request_amount - tolerance
        if min_request < 0:
            min_request = 0
        max_request = request_amount + tolerance

        for fund in FundAmount.query.all():
            if len(fund.amounts) > 1:
                kde = scipy.stats.gaussian_kde(fund.amounts, 0.1)
                result[fund.fund_slug] = kde.integrate_box_1d(min_request, max_request)
            else:
                result[fund.fund_slug] = 0
        return result
