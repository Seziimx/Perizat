import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'  # Use SQLite for simplicity
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static/uploads')
