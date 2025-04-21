from ..database import db
from flask_login import current_user

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apartment_id = db.Column(db.Integer, db.ForeignKey('apartment.id'), nullable=False)
    tenant_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    tenant = db.relationship('User', backref=db.backref('reviews', lazy=True))

    def __repr__(self):
        return f"<Review for Apartment {self.apartment_id} by Tenant {self.tenant_id}>"
