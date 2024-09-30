from app import db

def reset_db():
    with db.app.app_context():
        db.drop_all()
        db.create_all()

if __name__ == '__main__':
    reset_db()
