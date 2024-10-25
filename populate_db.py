#!/usr/bin/python3
from afrotour import create_app, db
from afrotour.models.user import User

# Create app and app context for database interactions
app = create_app()

with app.app_context():
    # Drop all existing tables and create new ones (for fresh testing)
    db.drop_all()
    db.create_all()

    # Create sample users
    user1 = User(username='testuser1', email='testuser1@example.com', password='password123', created_at=None, is_admin=False)
    user2 = User(username='adminuser', email='admin@example.com', password='adminpassword', created_at=None, is_admin=True)

    # Add users to the session
    db.session.add(user1)
    db.session.add(user2)

    # Commit the session to save the users in the database
    db.session.commit()

    print("Database populated with test data.")
