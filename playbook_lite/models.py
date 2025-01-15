"""SQLAlchemy models for the interactive storytelling platform"""
from datetime import datetime
from typing import Dict, List
import logging
from sqlalchemy import JSON, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from playbook_lite.database import db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TimelineNodeModel(db.Model):
    """Database model for timeline nodes with focus on content"""
    __tablename__ = 'timeline_nodes'

    id: Mapped[str] = mapped_column(String(50), primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    summary: Mapped[str] = mapped_column(String(1000))
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    characters_present: Mapped[List[str]] = mapped_column(JSON)
    next_nodes: Mapped[List[str]] = mapped_column(JSON)

    # Story progression tracking
    is_branch_point: Mapped[bool] = mapped_column(Boolean, default=False)
    thematic_elements: Mapped[Dict] = mapped_column(JSON, default=dict)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initialize with better error handling"""
        try:
            super().__init__(**kwargs)
        except Exception as e:
            logger.error(f"Error initializing TimelineNodeModel: {str(e)}")
            raise

    def __repr__(self):
        return f"<TimelineNode {self.id}: {self.title}>"

class StoryStateModel(db.Model):
    """Database model for tracking overall story state"""
    __tablename__ = 'story_states'

    id: Mapped[int] = mapped_column(primary_key=True)
    current_node_id: Mapped[str] = mapped_column(ForeignKey('timeline_nodes.id'))
    active_themes: Mapped[Dict] = mapped_column(JSON, default=dict)
    character_states: Mapped[Dict] = mapped_column(JSON, default=dict)

    # Save/Load metadata
    save_slot: Mapped[int] = mapped_column(default=1)
    save_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        """Initialize with better error handling"""
        try:
            super().__init__(**kwargs)
        except Exception as e:
            logger.error(f"Error initializing StoryStateModel: {str(e)}")
            raise

    def __repr__(self):
        return f"<StoryState {self.id} at node {self.current_node_id}>"