"""Database initialization and configuration for the interactive storytelling platform"""
import os
import logging
from urllib.parse import urlparse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    """Base class for SQLAlchemy models"""
    pass

# Initialize SQLAlchemy with the Base class
db = SQLAlchemy(model_class=Base)

def init_db(app):
    """Initialize database with application context"""
    try:
        logger.info("Initializing database connection")

        # Get database URL from environment
        db_url = os.getenv('DATABASE_URL')
        if not db_url:
            raise ValueError("DATABASE_URL environment variable is not set")

        # Configure SQLAlchemy
        app.config['SQLALCHEMY_DATABASE_URI'] = db_url
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
            'pool_size': 5,
            'pool_timeout': 30,
            'pool_recycle': 1800,  # Recycle connections after 30 minutes
            'pool_pre_ping': True
        }

        logger.info("Initializing Flask-SQLAlchemy")
        db.init_app(app)

        # Test the connection within app context
        with app.app_context():
            logger.info("Testing database connection")
            result = db.session.execute('SELECT 1')
            db.session.commit()
            logger.info("Database connection verified successfully")

        return True

    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}", exc_info=True)
        raise