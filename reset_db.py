from app import app, db  # Ensure your app and db are imported correctly

def reset_db():
    # Create an app context to access db
    with app.app_context():
        db.drop_all()  # Drop all existing tables
        db.create_all()  # Create all tables defined in your models

if __name__ == '__main__':
    reset_db()