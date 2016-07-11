import os
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics.pairwise import pairwise_distances


class Recommender:

    def read_json(self):
        # todo endpoint by env & authentication
        return pd.read_json('http://localhost:3000/v1/insight/grants')

    def beneficiaries(self):
        df = self.read_json()
        df.set_index('recipient', inplace=True)
        df.drop('fund', inplace=True, axis=1)
        return df

    def grants(self):
        df = self.read_json()
        df = df[['fund', 'recipient']]
        df.set_index('recipient', inplace=True)
        return df

    def funder_beneficiaries(self, beneficiaries, grants):
        df = grants.join(beneficiaries)
        df = df.dropna()
        df.reset_index(drop=True, inplace=True)
        return df.groupby('fund').sum()

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
            instance.update(*data)
            return instance
        else:
            instance = model(*data)
            session.add(instance)
            session.commit()
            return instance

    def save_funders_data(self):
        from app import db
        from models import FunderBeneficiary
        df = self.prepare_funders_data()
        for row in df.itertuples():
            self.get_or_create(db.session, FunderBeneficiary, row[0], row)

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
        funders_df.set_index('fund', inplace=True)
        distances = pairwise_distances(parsed_user_input, funders_df, metric='cosine', n_jobs=1)
        return pd.Series(1 - distances[0], index=funders_df.index)
