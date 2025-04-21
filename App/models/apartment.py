from ..database import db

class Apartment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    amenities = db.Column(db.String(255))  # comma-separated values or tags
    price = db.Column(db.Float, nullable=False)
    landlord_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviews = db.relationship('Review', backref='apartment', lazy=True)
    landlord = db.relationship('User', backref=db.backref('apartments', lazy=True))

    def __repr__(self):
        return f"<Apartment {self.name}>"