from afrotour import db


class Tour(db.Model):
    """
    Model for a tour in the Afrotour app.

    Attributes:
        id (int): The primary key identifier for the tour.
        name (str): The name of the tour (max 150 characters).
        description (str): A detailed description of the tour.
        category (str): The category to which the tour belongs.
        price (float): The price of the tour.
        start_date (date): The start date of the tour.
        end_date (date): The end date of the tour.
        images (str): A comma-separated string of image URLs for the tour.
        itinerary (str): The itinerary of the tour.
        reviews (list): A relationship field to access reviews associated with the tour.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(150))
    price = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    images = db.Column(db.String(200))
    itinerary = db.Column(db.Text)
    reviews = db.relationship('Review', backref='tour', lazy=True)


class Review(db.Model):
    """
    Model for a review in the Afrotour app.

    Attributes:
        id (int): The primary key identifier for the review.
        tour_id (int): A foreign key that references the associated tour.
        content (str): The content of the review.
        rating (int): The rating given in the review (assumed to be an integer).
    """
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    content = db.Column(db.Text)
    rating = db.Column(db.Integer)
