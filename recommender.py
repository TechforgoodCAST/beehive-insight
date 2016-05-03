import os
import pandas as pd
from sklearn import preprocessing
from sklearn.metrics.pairwise import pairwise_distances

class Recommender:

    def __init__(self):
        self.data_path = os.environ.get('DATA_PATH') or ''

    def read_csv(self, year):
        filename = self.data_path + 'data/grants/grants_' + str(year) + '.csv'
        return pd.read_csv(filename)

    def beneficiaries_for(self, year):
        df = self.read_csv(year)
        df.set_index('recipient', inplace=True)
        df.drop('funder', inplace=True, axis=1)
        return df

    def grants_for(self, year):
        df = self.read_csv(year)
        df = df[['funder', 'recipient']]
        df.set_index('recipient', inplace=True)
        return df

    def funder_beneficiaries(self, beneficiaries, grants):
    	df = grants.join(beneficiaries)
    	df = df.dropna()
    	df.reset_index(drop=True, inplace=True)
    	return df.groupby('funder').sum()

    def scale_funder_beneficiaries(self, funder_beneficiaries_groups):
    	min_max_scaler = preprocessing.MinMaxScaler()
    	X_train_minmax = min_max_scaler.fit_transform(funder_beneficiaries_groups)
    	return pd.DataFrame(X_train_minmax, columns=funder_beneficiaries_groups.columns, index=funder_beneficiaries_groups.index)

    def prepare_funders_data(self, year):
        beneficiaries = self.beneficiaries_for(year)
        grants = self.grants_for(year)
        funder_beneficiaries_groups = self.funder_beneficiaries(beneficiaries, grants)
        scaled_funder_beneficiaries_groups = self.scale_funder_beneficiaries(funder_beneficiaries_groups)
        scaled_funder_beneficiaries_groups.to_csv(self.data_path + 'data/scaled/scaled_2014.csv')
        return scaled_funder_beneficiaries_groups

    def parse_user_input(self, user_input):
        categories = [
            'animals',      'buildings',     'care',        'crime',
            'disabilities', 'disasters',     'education',   'environment',
            'ethnic',       'exploitation',  'food',        'housing',
            'mental',       'organisations', 'orientation', 'physical',
            'poverty',      'public',        'refugees',    'relationship',
            'religious',    'services',      'unemployed',  'water'
        ]
        for k, v in user_input.items():
            categories[categories.index(k)] = v
        return categories

    def recommend_funders(self, year, user_input):
        parsed_user_input = self.parse_user_input(user_input)
        filename = self.data_path + 'data/scaled/scaled_' + str(year) + '.csv'
        file_present = os.path.isfile(filename)
        if file_present:
            funders_data = pd.read_csv(filename)
        else:
            funders_data = self.prepare_funders_data(year)
        funders_data = self.prepare_funders_data(year)
        distances = pairwise_distances(parsed_user_input, funders_data, metric='cosine', n_jobs=1)
        return pd.Series(1-distances[0], index=funders_data.index)
