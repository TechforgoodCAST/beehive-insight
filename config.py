import os


class Base(object):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BEEHIVE_DATA_ENDPOINT = os.environ.get('BEEHIVE_DATA_ENDPOINT')
    BEEHIVE_DATA_TOKEN = os.environ.get('BEEHIVE_DATA_TOKEN')


class Development(Base):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://localhost/beehive_insight_development'
    BEEHIVE_DATA_ENDPOINT = 'http://localhost:3000/v1/insight/grants'


class Production(Base):
    DEBUG = True
