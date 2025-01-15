"""Database migrations for the interactive storytelling platform"""
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import logging
from playbook_lite.database import db
from playbook_lite.models import TimelineNodeModel, StoryStateModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_migrations(app: Flask) -> None:
    """Initialize database migrations"""
    try:
        logger.info("Initializing database migrations...")

        # Initialize Flask-Migrate
        migrate = Migrate(app, db)

        # Import models to ensure they're tracked by migrations
        TimelineNodeModel
        StoryStateModel

        logger.info("Database migrations initialized successfully")

    except Exception as e:
        logger.error(f"Error initializing migrations: {str(e)}")
        raise