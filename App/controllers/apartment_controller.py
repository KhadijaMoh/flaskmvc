from ..database import db
from ..models.apartment import Apartment

def create_apartment(name, location, amenities, price, landlord_id):
    amenities_str = ','.join(amenities) if amenities else ''
    new_apartment = Apartment(
        name=name,
        location=location,
        amenities=amenities_str,
        price=price,
        landlord_id=landlord_id
    )
    db.session.add(new_apartment)
    db.session.commit()
    return new_apartment

def get_all_apartments():
    return Apartment.query.all()

def get_apartment_by_id(apartment_id):
    return Apartment.query.get_or_404(apartment_id)

def update_apartment(apartment, name, location, amenities, price):
    amenities_str = ','.join(amenities) if amenities else ''
    apartment.name = name
    apartment.location = location
    apartment.amenities = amenities_str
    apartment.price = price
    db.session.commit()
    return True

def delete_apartment(apartment):
    db.session.delete(apartment)
    db.session.commit()
    return True

def filter_apartments(location, amenities):
    query = Apartment.query

    if location:
        query = query.filter(Apartment.location.ilike(f'%{location}%'))

    if amenities:
        for amenity in amenities:
            query = query.filter(Apartment.amenities.ilike(f'%{amenity.strip()}%'))

    return query.all()