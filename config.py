import os


class Base(object):
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BEEHIVE_DATA_ENDPOINT = os.environ.get('BEEHIVE_DATA_ENDPOINT')
    BEEHIVE_DATA_AMOUNT_ENDPOINT = os.environ.get('BEEHIVE_DATA_AMOUNT_ENDPOINT')
    BEEHIVE_DATA_DURATION_ENDPOINT = os.environ.get('BEEHIVE_DATA_DURATION_ENDPOINT')
    BEEHIVE_DATA_TOKEN = os.environ.get('BEEHIVE_DATA_TOKEN')
    BEEHIVE_INSIGHT_TOKEN = os.environ.get('BEEHIVE_INSIGHT_TOKEN')
    BEEHIVE_INSIGHT_SECRET = os.environ.get('BEEHIVE_INSIGHT_SECRET')


class Development(Base):
    DEBUG = True
    SECRET_KEY = 'secret'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://localhost/beehive_insight_development'
    BEEHIVE_DATA_ENDPOINT = 'http://localhost:3001/v1/integrations/beneficiaries'
    BEEHIVE_DATA_AMOUNT_ENDPOINT = 'http://localhost:3001/v1/integrations/amounts'
    BEEHIVE_DATA_DURATION_ENDPOINT = 'http://localhost:3001/v1/integrations/durations'
    BEEHIVE_INSIGHT_TOKEN = 'username'
    BEEHIVE_INSIGHT_SECRET = 'password'


class Staging(Base):
    DEBUG = True


class Production(Base):
    DEBUG = False
