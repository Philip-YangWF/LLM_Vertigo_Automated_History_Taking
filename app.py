from flask import Flask
from models import db
from routes import screening_bp, results_bp
from dashboard import init_dashboard  # For Dash integration

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SECRET_KEY'] = 'supersecretkey'

# Initialize the database
db.init_app(app)

# Register the blueprints for routes
app.register_blueprint(screening_bp)
app.register_blueprint(results_bp)

# Initialize the Dash app inside Flask
dash_app = init_dashboard(app)

# Create database tables
def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_tables()
    app.run(debug=True,port= 5001)
