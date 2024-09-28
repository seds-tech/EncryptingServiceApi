from flask import Flask
from flask_mongoengine import MongoEngine
from config import Config

db = MongoEngine()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    
    if not app.config['MONGODB_SETTINGS']['host']:
        print("MONGO_URI is not set in the configuration!")
        return app

    try:
        # Initialize MongoDB connection
        db.init_app(app)
        print("MongoDB connection successful")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        print(f"Type of error: {type(e)}")
    
    # Import and register blueprints
    from app.routes import main_blueprint
    app.register_blueprint(main_blueprint)
    
    return app