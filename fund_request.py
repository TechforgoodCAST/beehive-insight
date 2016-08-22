import os
import requests
import pandas as pd
import scipy.stats


class FundRequest:

    def __init__(self):
        import config
        env = os.environ.get('APP_ENV') or 'Development'
        self.config = getattr(config, env)

    def __read_json(self, endpoint):
        if endpoint == 'amounts':
            url = self.config.BEEHIVE_DATA_AMOUNT_ENDPOINT
        elif endpoint == 'durations':
            url = self.config.BEEHIVE_DATA_DURATION_ENDPOINT
        token = self.config.BEEHIVE_DATA_TOKEN
        headers = {'Authorization': 'Token token=' + token}
        response = requests.get(url, headers=headers)
        df = pd.read_json(response.text)
        df.set_index('fund_slug', inplace=True)
        return df

    # TODO: refactor
    def __get_or_create(self, model, slug, data, field):
        from app import db
        session = db.session
        instance = model.query.filter_by(fund_slug=slug).first()
        if instance:
            instance.update(data)
            session.commit()
            return instance
        else:
            instance = model(slug, data[field])
            session.add(instance)
            session.commit()
            return instance

    def __save(self, model, endpoint):
        df = self.__read_json(endpoint)
        dic = df.to_dict(orient='index')
        for item in dic.items():
            self.__get_or_create(model, item[0], item[1], endpoint)

    def __serialized(self, model):
        records = []
        for record in model.query.order_by(model.fund_slug).all():
            records.append(record.serialize)
        return records

    def save_fund_amounts(self):
        from models import FundAmount
        self.__save(FundAmount, 'amounts')
        return self.__serialized(FundAmount)

    def save_fund_durations(self):
        from models import FundDuration
        self.__save(FundDuration, 'durations')
        return self.__serialized(FundDuration)

    def __generate_scores(self, model, field, request, tolerance, bandwidth=0.1):
        result = {}
        min_request = request - tolerance
        if min_request < 0:
            min_request = 0
        max_request = request + tolerance

        for fund in model.query.all():
            if len(set(getattr(fund, field))) > 1:
                kde = scipy.stats.gaussian_kde(getattr(fund, field), bandwidth)
                result[fund.fund_slug] = kde.integrate_box_1d(min_request, max_request)
            else:
                result[fund.fund_slug] = 0
        return result

    def check_amount(self, request_amount):
        from models import FundAmount
        result = self.__generate_scores(FundAmount, 'amounts', request_amount, 10000)
        return result

    def check_duration(self, request_duration):
        from models import FundDuration
        result = self.__generate_scores(FundDuration, 'durations', request_duration, 1)
        return result
