import os


class Base(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BEEHIVE_DATA_ENDPOINT = os.environ.get('BEEHIVE_DATA_ENDPOINT')
    BEEHIVE_DATA_AMOUNT_ENDPOINT = os.environ.get('BEEHIVE_DATA_AMOUNT_ENDPOINT')
    BEEHIVE_DATA_TOKEN = os.environ.get('BEEHIVE_DATA_TOKEN')
    BEEHIVE_INSIGHT_TOKEN = os.environ.get('BEEHIVE_INSIGHT_TOKEN')
    BEEHIVE_INSIGHT_SECRET = os.environ.get('BEEHIVE_INSIGHT_SECRET')


class Development(Base):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://localhost/beehive_insight_development'
    BEEHIVE_DATA_ENDPOINT = 'http://localhost:3000/v1/insight/grants'
    BEEHIVE_DATA_AMOUNT_ENDPOINT = 'http://localhost:3000/v1/integrations/amounts'
    BEEHIVE_INSIGHT_TOKEN = 'username'
    BEEHIVE_INSIGHT_SECRET = 'password'


class Production(Base):
    DEBUG = False
