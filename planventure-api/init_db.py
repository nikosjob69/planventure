from app import create_app
from user_model import db
from trip_model import Trip


def init_db():
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")


if __name__ == "__main__":
    init_db()
