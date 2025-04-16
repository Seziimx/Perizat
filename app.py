from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from database.models import db  # Import the single SQLAlchemy instance
from routes.equipment_routes import equipment_bp
from routes.auth_routes import auth_bp
from routes.report_routes import report_bp
from routes.dashboard_routes import dashboard_bp
from routes.calendar_routes import calendar_bp  # Import the calendar blueprint
from routes.three_d_routes import three_d_bp  # Import the new blueprint

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'

# Initialize database
db.init_app(app)  # Ensure the SQLAlchemy instance is initialized with the app

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
app.register_blueprint(equipment_bp, url_prefix='/equipment')
app.register_blueprint(report_bp, url_prefix='/reports')
app.register_blueprint(calendar_bp, url_prefix='/calendar')  # Register the calendar blueprint
app.register_blueprint(three_d_bp, url_prefix='/3d')  # Register the 3D visualization blueprint

@app.route('/')
def index():
    return redirect(url_for('auth_bp.login'))  # Redirect to the login page

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)

