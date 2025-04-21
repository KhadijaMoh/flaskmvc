from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import ApartmentForm
from ..controllers.apartment_controller import (
    create_apartment, get_all_apartments, get_apartment_by_id,
    update_apartment, delete_apartment, filter_apartments
)
from ..models.apartment import Apartment  # Import the model for type hinting or direct checks

apartments_bp = Blueprint('apartments', __name__, url_prefix='/apartments', template_folder='templates')

@apartments_bp.route('/')
def index():
    apartments = get_all_apartments()
    return render_template('index.html', apartments=apartments)

@apartments_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_apartment():
    if current_user.is_authenticated and current_user.role == 'landlord':
        form = ApartmentForm()
        if form.validate_on_submit():
            apartment = create_apartment(
                form.name.data, form.location.data, form.amenities.data,
                form.price.data, current_user.id
            )
            flash('Apartment listing created successfully!', 'success')
            return redirect(url_for('apartments.index'))
        return render_template('create_apartment.html', title='New Apartment', form=form)
    else:
        flash('You do not have permission to create apartment listings.', 'danger')
        return redirect(url_for('apartments.index'))

@apartments_bp.route('/<int:apartment_id>')
def apartment_detail(apartment_id):
    apartment = get_apartment_by_id(apartment_id)
    return render_template('apartment_detail.html', apartment=apartment)

@apartments_bp.route('/edit/<int:apartment_id>', methods=['GET', 'POST'])
@login_required
def edit_apartment(apartment_id):
    apartment = get_apartment_by_id(apartment_id)
    if current_user.is_authenticated and (apartment.landlord_id == current_user.id or current_user.role == 'admin'):
        form = ApartmentForm(obj=apartment)
        if form.validate_on_submit():
            if update_apartment(apartment, form.name.data, form.location.data, form.amenities.data, form.price.data):
                flash('Apartment listing updated successfully!', 'success')
                return redirect(url_for('apartments.apartment_detail', apartment_id=apartment_id))
        form.amenities.data = apartment.amenities.split(',') if apartment.amenities else []
        return render_template('edit_apartment.html', title='Edit Apartment', form=form, apartment=apartment)
    else:
        flash('You do not have permission to edit this apartment listing.', 'danger')
        return redirect(url_for('apartments.apartment_detail', apartment_id=apartment_id))

@apartments_bp.route('/delete/<int:apartment_id>', methods=['POST'])
@login_required
def delete_apartment(apartment_id):
    apartment = get_apartment_by_id(apartment_id)
    if current_user.is_authenticated and (apartment.landlord_id == current_user.id or current_user.role == 'admin'):
        if delete_apartment(apartment):
            flash('Apartment listing deleted successfully!', 'success')
            return redirect(url_for('apartments.index'))
    else:
        flash('You do not have permission to delete this apartment listing.', 'danger')
        return redirect(url_for('apartments.apartment_detail', apartment_id=apartment_id))

@apartments_bp.route('/filter', methods=['GET'])
def filter_apartments_route():
    location = request.args.get('location')
    amenities = request.args.getlist('amenities')

    apartments = filter_apartments(location, amenities)
    return render_template('index.html', apartments=apartments)