"""Common type definitions for the story engine"""
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import logging

@dataclass
class CharacterAction:
    """Represents a specific character action that impacts the story"""
    character_id: str
    action_text: str
    impact_level: float  # 0.0 to 1.0
    thematic_elements: Dict[str, float]
    consequences: List[str]  # IDs of potential next timeline nodes
    is_canonical: bool = False

@dataclass
class StoryState:
    """Tracks the current state of the narrative"""
    current_node_id: str
    canonical_drift: float  # 0.0 = canonical, 1.0 = completely divergent
    active_themes: Dict[str, float]
    character_states: Dict[str, Dict[str, float]]
    available_actions: List[CharacterAction]

    # Save/Load metadata
    story_id: str = field(default="default_story")
    save_slot: int = field(default=1)
    save_time: str = field(default_factory=lambda: datetime.now().isoformat())
    version: str = field(default="1.0")

    def to_dict(self) -> Dict:
        """Convert StoryState to dictionary for serialization"""
        return {
            "metadata": {
                "story_id": self.story_id,
                "save_slot": self.save_slot,
                "save_time": self.save_time,
                "version": self.version
            },
            "state": {
                "current_node_id": self.current_node_id,
                "canonical_drift": self.canonical_drift,
                "active_themes": self.active_themes,
                "character_states": self.character_states,
                "available_actions": [
                    {
                        "character_id": action.character_id,
                        "action_text": action.action_text,
                        "impact_level": action.impact_level,
                        "thematic_elements": action.thematic_elements,
                        "consequences": action.consequences,
                        "is_canonical": action.is_canonical
                    }
                    for action in self.available_actions
                ]
            }
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'StoryState':
        """Create StoryState from dictionary"""
        metadata = data.get("metadata", {})
        state = data.get("state", {})

        # Convert action dictionaries back to CharacterAction objects
        actions = [
            CharacterAction(
                character_id=action["character_id"],
                action_text=action["action_text"],
                impact_level=action["impact_level"],
                thematic_elements=action["thematic_elements"],
                consequences=action["consequences"],
                is_canonical=action.get("is_canonical", False)
            )
            for action in state.get("available_actions", [])
        ]

        return cls(
            story_id=metadata.get("story_id", "default_story"),
            save_slot=metadata.get("save_slot", 1),
            save_time=metadata.get("save_time", datetime.now().isoformat()),
            version=metadata.get("version", "1.0"),
            current_node_id=state.get("current_node_id", ""),
            canonical_drift=state.get("canonical_drift", 0.0),
            active_themes=state.get("active_themes", {}),
            character_states=state.get("character_states", {}),
            available_actions=actions
        )

@dataclass
class TimelineNode:
    """Represents a single point in the story timeline"""
    id: str
    title: str
    description: str
    date: str  # ISO format date
    characters_present: List[str]
    next_nodes: List[str]
    requirements: Dict[str, float]  # Character state requirements
    tension_level: float = 0.0  # Overall narrative tension at this point
    thematic_elements: Dict[str, float] = field(default_factory=dict)  # Thematic consistency tracking
    is_branch_point: bool = False  # Whether this node represents a major decision
    branch_consequences: Dict[str, str] = field(default_factory=dict)  # Potential outcomes of choices
    character_actions: Dict[str, List[CharacterAction]] = field(default_factory=dict)  # Available character actions
    time_of_day: str = "unknown"  # Time of day for the scene
    duration: Optional[int] = None  # Duration of the scene in minutes

    def to_dict(self) -> Dict:
        """Convert node to dictionary for JSON serialization"""
        try:
            return {
                "id": self.id,
                "title": self.title,
                "description": self.description,
                "date": self.date,
                "characters": self.characters_present,
                "next_nodes": self.next_nodes,
                "tension_level": self.tension_level,
                "thematic_elements": self.thematic_elements,
                "is_branch_point": self.is_branch_point,
                "time_of_day": self.time_of_day,
                "duration": self.duration
            }
        except Exception as e:
            logging.error(f"Error serializing TimelineNode: {str(e)}")
            # Return minimal valid data structure if serialization fails
            return {
                "id": self.id,
                "title": "Error loading node",
                "description": "Data serialization error",
                "date": self.date,
                "characters": [],
                "next_nodes": []
            }