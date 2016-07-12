from app import db


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
    year = db.Column(db.Integer, nullable=False)
    for category in CATEGORIES:
        setattr(db.Model, category, db.Column(db.Float, nullable=False))

    def __init__(self, fund_slug, data):
        self.fund_slug = fund_slug
        self.year = fund_slug[0:4]
        for category in self.CATEGORIES:
            setattr(self, category, data[category])

    def __repr__(self):
        return '<FunderBeneficiary %r>' % self.id

    def update(self, data):
        for key in data.keys():
            setattr(self, key, data[key])

    @property
    def serialize(self):
        response = {'fund_slug': self.fund_slug}
        for category in self.CATEGORIES:
            response[category] = getattr(self, category)
        return response
