import os
import requests
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics.pairwise import pairwise_distances


class Recommender:

    def __init__(self):
        import config
        env = os.environ.get('APP_ENV') or 'Development'
        self.config = getattr(config, env)

    def read_json(self):
        url = self.config.BEEHIVE_DATA_ENDPOINT
        token = self.config.BEEHIVE_DATA_TOKEN
        headers = {'Authorization': 'Token token=' + token}
        response = requests.get(url, headers=headers)
        return pd.read_json(response.text)

    def beneficiaries(self):
        df = self.read_json()
        df.set_index('recipient', inplace=True)
        df.drop('fund_slug', inplace=True, axis=1)
        return df

    def grants(self):
        df = self.read_json()
        df = df[['fund_slug', 'recipient']]
        df.set_index('recipient', inplace=True)
        return df

    def funder_beneficiaries(self, beneficiaries, grants):
        df = grants.join(beneficiaries)
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        return df.groupby('fund_slug').sum()

    def scale_funder_beneficiaries(self, funder_beneficiaries_groups):
        min_max_scaler = preprocessing.MinMaxScaler()
        X_train_minmax = min_max_scaler.fit_transform(funder_beneficiaries_groups)
        return pd.DataFrame(X_train_minmax, columns=funder_beneficiaries_groups.columns, index=funder_beneficiaries_groups.index)

    def prepare_funders_data(self):
        funder_beneficiaries_groups = self.funder_beneficiaries(self.beneficiaries(), self.grants())
        scaled_funder_beneficiaries_groups = self.scale_funder_beneficiaries(funder_beneficiaries_groups)
        return scaled_funder_beneficiaries_groups

    def get_or_create(self, session, model, slug, data):
        instance = session.query(model).filter_by(fund_slug=slug).first()
        if instance:
            instance.update(data)
            session.commit()
            return instance
        else:
            instance = model(slug, data)
            session.add(instance)
            session.commit()
            return instance

    def save_funders_data(self):
        from app import db
        from models import FunderBeneficiary
        df = self.prepare_funders_data()
        dic = df.to_dict(orient='index')
        for item in dic.items():
            self.get_or_create(db.session, FunderBeneficiary, item[0], item[1])

    def parse_user_input(self, user_input):
        from models import FunderBeneficiary
        categories = []
        for category in FunderBeneficiary.CATEGORIES:
            categories.append(category)
        for k, v in user_input.items():
            categories[categories.index(k)] = v
        return categories

    def recommend_funders(self, user_input):
        from models import FunderBeneficiary
        parsed_user_input = self.parse_user_input(user_input)
        funders_data = []
        for record in FunderBeneficiary.query.all():
            funders_data.append(record.serialize)
        funders_df = pd.DataFrame(funders_data)
        funders_df.set_index('fund_slug', inplace=True)
        distances = pairwise_distances(parsed_user_input, funders_df, metric='cosine', n_jobs=1)
        return pd.Series(1 - distances[0], index=funders_df.index)
