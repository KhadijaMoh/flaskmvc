from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import ReviewForm
from ..controllers.review_controller import create_review, get_review_by_id, update_review, delete_review
from ..models.apartment import Apartment  # Import for checking apartment existence

reviews_bp = Blueprint('reviews', __name__, url_prefix='/reviews', template_folder='templates')

@reviews_bp.route('/new/<int:apartment_id>', methods=['GET', 'POST'])
@login_required
def new_review(apartment_id):
    if current_user.is_authenticated and current_user.role == 'tenant':
        apartment = Apartment.query.get_or_404(apartment_id)
        form = ReviewForm()
        if form.validate_on_submit():
            create_review(form.rating.data, form.comment.data, apartment_id, current_user.id)
            flash('Your review has been submitted!', 'success')
            return redirect(url_for('apartments.apartment_detail', apartment_id=apartment_id))
        return render_template('create_review.html', title='Add Review', form=form, apartment=apartment)
    else:
        flash('Only verified tenants can write reviews.', 'danger')
        return redirect(url_for('apartments.apartment_detail', apartment_id=apartment_id))

@reviews_bp.route('/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def edit_review(review_id):
    review = get_review_by_id(review_id)
    if current_user.is_authenticated and review.tenant_id == current_user.id:
        form = ReviewForm(obj=review)
        if form.validate_on_submit():
            update_review(review, form.rating.data, form.comment.data)
            flash('Your review has been updated!', 'success')
            return redirect(url_for('apartments.apartment_detail', apartment_id=review.apartment_id))
        return render_template('edit_review.html', title='Edit Review', form=form, review=review)
    else:
        flash('You do not have permission to edit this review.', 'danger')
        return redirect(url_for('apartments.apartment_detail', apartment_id=review.apartment_id))

@reviews_bp.route('/delete/<int:review_id>', methods=['POST'])
@login_required
def delete_review(review_id):
    review = get_review_by_id(review_id)
    if current_user.is_authenticated and (review.tenant_id == current_user.id or current_user.role == 'admin'):
        delete_review(review)
        flash('Review deleted successfully!', 'success')
        return redirect(url_for('apartments.apartment_detail', apartment_id=review.apartment_id))
    else:
        flash('You do not have permission to delete this review.', 'danger')
        return redirect(url_for('apartments.apartment_detail', apartment_id=review.apartment_id))