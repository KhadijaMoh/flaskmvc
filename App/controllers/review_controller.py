from ..database import db
from ..models.review import Review

def create_review(rating, comment, apartment_id, tenant_id):
    new_review = Review(
        rating=rating,
        comment=comment,
        apartment_id=apartment_id,
        tenant_id=tenant_id
    )
    db.session.add(new_review)
    db.session.commit()
    return new_review

def get_review_by_id(review_id):
    return Review.query.get_or_404(review_id)

def update_review(review, rating, comment):
    review.rating = rating
    review.comment = comment
    db.session.commit()
    return True

def delete_review(review):
    db.session.delete(review)
    db.session.commit()
    return True