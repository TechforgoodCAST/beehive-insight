from app import db
import sqlalchemy
from sqlalchemy.dialects.postgresql import ARRAY


class FunderBeneficiary(db.Model):

    __tablename__ = 'funder_beneficiaries'

    CATEGORIES = [
        'animals', 'buildings', 'care', 'crime', 'disabilities',
        'disasters', 'education', 'environment', 'ethnic', 'exploitation',
        'food', 'housing', 'mental', 'organisation', 'organisations',
        'orientation', 'physical', 'poverty', 'public', 'refugees',
        'relationship', 'religious', 'services', 'unemployed', 'water'
    ]

    id = db.Column(db.Integer, primary_key=True)
    fund_slug = db.Column(db.String(255), nullable=False)
    manual = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, fund_slug, data, manual=False):
        self.fund_slug = fund_slug
        self.manual = manual
        for category in self.CATEGORIES:
            setattr(self, category, data[category])

    def __repr__(self):
        return '<FunderBeneficiary %r>' % self.id

    # TODO: refactor
    def update(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    @property
    def serialize(self):
        response = {'fund_slug': self.fund_slug, 'manual': self.manual}
        for category in self.CATEGORIES:
            response[category] = getattr(self, category)
        return response

for category in FunderBeneficiary.CATEGORIES:
    setattr(FunderBeneficiary, category, db.Column(db.Float, nullable=False))


class FundAmount(db.Model):

    __tablename__ = 'fund_amount'

    id = db.Column(db.Integer, primary_key=True)
    fund_slug = db.Column(db.String(255), nullable=False)
    amounts = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Float), nullable=False)

    def __init__(self, fund_slug, amounts):
        self.fund_slug = fund_slug
        self.amounts = amounts

    def __repr__(self):
        return '<FundAmount %r>' % self.id

    # TODO: refactor
    def update(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    @property
    def serialize(self):
        return {
            'fund_slug': self.fund_slug,
            'amounts': self.amounts
        }


class FundDuration(db.Model):

    __tablename__ = 'fund_duration'

    id = db.Column(db.Integer, primary_key=True)
    fund_slug = db.Column(db.String(255), nullable=False)
    durations = db.Column(sqlalchemy.dialects.postgresql.ARRAY(db.Float), nullable=False)

    def __init__(self, fund_slug, durations):
        self.fund_slug = fund_slug
        self.durations = durations

    def __repr__(self):
        return '<FundDuration %r>' % self.id

    # TODO: refactor
    def update(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    @property
    def serialize(self):
        return {
            'fund_slug': self.fund_slug,
            'durations': self.durations
        }
