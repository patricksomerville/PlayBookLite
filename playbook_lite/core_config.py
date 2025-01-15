"""Core configuration and design principles for PlayBook.

This module should be imported by all APIs to maintain consistent behavior
and design philosophy across the system.
"""

from typing import Dict, Any
from dataclasses import dataclass, field
from enum import Enum

class InterfaceStyle(Enum):
    """Defines the presentation style for different aspects of the game"""
    COMMAND = "DOS-style command prompt"
    RESPONSE = "Classic text adventure response"
    ERROR = "Period-appropriate error message"
    INVENTORY = "Simple item list"
    MAP = "ASCII art map"
    STATS = "Basic character stats display"

@dataclass
class CoreDesignPrinciples:
    """Core design principles that should guide all API behaviors"""
    
    # Surface presentation should always feel like a 1980s text adventure
    INTERFACE_STYLE: Dict[str, str] = field(default_factory=lambda: {
        "prompt": ">",
        "background": "black",
        "foreground": "white",
        "font": "DOS-like monospace",
        "width": "80 characters",
        "height": "25 lines"
    })
    
    # Basic commands that mask complex processing
    BASIC_COMMANDS: Dict[str, str] = field(default_factory=lambda: {
        "LOOK": "Triggers environmental analysis, character state evaluation, and theme recognition",
        "GO": "Activates navigation system, position tracking, and scene transition logic",
        "TALK": "Initiates character interaction system, relationship tracking, and dialogue generation",
        "USE": "Engages item interaction system, consequence calculation, and state updates",
        "INVENTORY": "Displays carried items and their narrative significance",
        "HELP": "Shows basic commands while hiding system complexity"
    })
    
    # Sophisticated systems masked by simple interface
    HIDDEN_SYSTEMS: Dict[str, str] = field(default_factory=lambda: {
        "character_modeling": "Full psychological and emotional state tracking",
        "environmental_engine": "Weather, physics, and nautical calculations",
        "narrative_branching": "Story divergence and theme preservation system",
        "literary_analysis": "Theme, symbol, and metaphor recognition",
        "causal_chain": "Action-consequence relationship tracking",
        "historical_accuracy": "Period detail verification system"
    })

class ResponseFormatter:
    """Formats complex system outputs as simple text adventure responses"""
    
    @staticmethod
    def format_room_description(
        environment_data: Dict[str, Any],
        character_states: Dict[str, Any],
        thematic_elements: Dict[str, Any]
    ) -> str:
        """Convert rich environmental and character data into simple room description"""
        # Implementation would go here
        pass
    
    @staticmethod
    def format_character_interaction(
        dialogue_data: Dict[str, Any],
        relationship_state: Dict[str, Any],
        narrative_context: Dict[str, Any]
    ) -> str:
        """Convert complex character interaction data into simple dialogue output"""
        # Implementation would go here
        pass
    
    @staticmethod
    def format_action_result(
        action_consequences: Dict[str, Any],
        state_changes: Dict[str, Any],
        thematic_impact: Dict[str, Any]
    ) -> str:
        """Convert complex action results into simple consequence description"""
        # Implementation would go here
        pass

# Global configuration that all APIs should use
PLAYBOOK_CONFIG = {
    "interface_style": InterfaceStyle,
    "design_principles": CoreDesignPrinciples(),
    "response_formatter": ResponseFormatter(),
    "max_response_length": 80,  # Characters per line
    "text_scroll_speed": 0.05,  # Seconds per character
    "save_format": "DOS-style save file",
    "error_style": "Period-appropriate error messages",
    "ascii_art_enabled": True,
    "sound_enabled": False  # Future expansion possibility
}

def get_config() -> Dict[str, Any]:
    """Get the global PlayBook configuration"""
    return PLAYBOOK_CONFIG
