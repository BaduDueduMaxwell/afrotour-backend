from flask import Blueprint, request, jsonify
from datetime import datetime
from afrotour.models import Tour
from afrotour import db

tour = Blueprint('tour', __name__)

@tour.route('/tours', methods=['GET'])
def get_tours():
    """
    Get a list of tours, optionally filtered by category,
    price range, and date range

    Parameters:
    - category: The category of the tours to filter by (optional).
    - min_price: The minimum price of the tours (optional).
    - max_price: The maximum price of the tours (optional).
    - start_date: The earliest start date for the tours (optional).
    - end_date: The latest end date for the tours (optional).

    Returns:
    A JSON response with a message and the list of tours.
    """
    data = request.get_json() or {}
    category = data.get('category')
    min_price = data.get('min_price')
    max_price = data.get('max_price')
    start_date = data.get('start_date')
    end_date = data.get('end_date')

    query = Tour.query

    if category:
        query = query.filter_by(category=category)
    if min_price:
        query = query.filter(Tour.price >= float(min_price))
    if max_price:
        query = query.filter(Tour.price <= float(max_price))
    if start_date:
        query = query.filter(Tour.start_date >= datetime.strptime(start_date, '%Y-%m-%d'))
    if end_date:
        query = query.filter(Tour.end_date <= datetime.strptime(end_date, '%Y-%m-%d'))

    tours = Tour.query.all()
    tour_data = [tour.to_dict() for tour in tours]

    return jsonify({
        "message": "Tours have been successfully retrieved",
        "data": tour_data
    })


def to_dict(self):
    """
    Convert the Tour instance into a dictionary format for JSON serialization.

    Returns:
    A dictionary representation of the Tour instance.
    """
    return {
        "id": self.id,
        "name": self.name,
        "description": self.description,
        "category": self.category,
        "price": self.price,
        "start_date": self.start_date.isoformat(),
        "end_date": self.end_date.isoformat(),
        "images": self.images.split(',') if self.images else [],
        "itinerary": self.itinerary
    }

Tour.to_dict = to_dict  # Attach the method to the Tour model


@tour.route('/search', methods=['GET'])
def search_tours():
    """
    Search for tours by a keyword in the name or description.

    Parameters:
    - keyword: The keyword to search for in the tour name and description.

    Returns:
    A JSON response with a list of tours that match the search criteria or a message if no tours are found.
    """
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"message": "Keyword is not found"}), 400

    tours = Tour.query.filter(
        (Tour.name.ilike(f'%{keyword}%')) | (Tour.description.ilike(f'%{keyword}%'))
    ).all()

    if not tours:
        return jsonify({"message": "No tours found matching the keyword."}), 404
    return jsonify([tour.to_dict() for tour in tours])


@tour.route('/<int:id>', methods=['GET'])
def get_tour(id):
    """
    Get the details of a specific tour by its ID.

    Parameters:
    - id: The ID of the tour to retrieve.

    Returns:
    A JSON response with the details of the requested tour.
    """
    tour = Tour.query.get_or_404(id)
    return jsonify(tour.to_dict())


@tour.route('/tours', methods=['POST'])
def add_tour():
    """
    Add a new tour to the database

    Request Body:
    A JSON object containing the tour details, including name, description,
    category, price, start_date, end_date, images, and itinerary.

    Returns:
    A JSON response with the details of the newly created tour.
    """
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    category = data.get('category')
    price = data.get('price')
    start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d')
    end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d')
    images = ','.join(data.get('images', []))  # Convert list to string
    itinerary = data.get('itinerary')

    # Create a new Tour object
    new_tour = Tour(
        name=name, description=description, category=category, price=price,
        start_date=start_date, end_date=end_date, images=images, itinerary=itinerary
    )
    db.session.add(new_tour)
    db.session.commit()
    return jsonify(new_tour.to_dict()), 201
