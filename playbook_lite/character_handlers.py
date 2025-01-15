"""Character-specific command handlers for PlayBook Lite."""

from typing import Dict, Optional, List
from dataclasses import dataclass
import random

@dataclass
class CharacterResponse:
    """Response from a character's perspective"""
    text: str
    special_insight: Optional[str] = None
    affected_themes: List[str] = None

class CharacterHandler:
    """Base class for character-specific command processing"""
    
    def __init__(self, name: str):
        self.name = name
        self.vocabulary: Dict[str, List[str]] = {}
        self.special_ability_chance = 0.3
    
    def process_command(self, command: str, location: str) -> CharacterResponse:
        """Process command through character's perspective"""
        raise NotImplementedError

class IshmaelHandler(CharacterHandler):
    """Processes commands through Ishmael's philosophical lens"""
    
    def __init__(self):
        super().__init__("ISHMAEL")
        self.vocabulary = {
            "observe": [
                "I notice with some interest...",
                "Upon careful consideration...",
                "As I stand here contemplating...",
            ],
            "reflect": [
                "This reminds me of a passage I once read...",
                "Perhaps there is deeper meaning here...",
                "In my wanderings, I've learned...",
            ]
        }
    
    def process_command(self, command: str, location: str) -> CharacterResponse:
        if "LOOK" in command:
            prefix = random.choice(self.vocabulary["observe"])
            if location == "waterfront":
                return CharacterResponse(
                    f"{prefix} the Pequod's weathered hull speaks of countless voyages. "
                    "Her name, taken from a vanished tribe of Indians, carries an air of doom. "
                    "The salt air mingles with tar and oakum, that peculiar perfume of the sea.",
                    special_insight="The ship's very name foreshadows extinction and loss.",
                    affected_themes=["fate", "identity"]
                )
        return CharacterResponse("I ponder my next move carefully.")

class QueequegHandler(CharacterHandler):
    """Processes commands through Queequeg's spiritual lens"""
    
    def __init__(self):
        super().__init__("QUEEQUEG")
        self.vocabulary = {
            "observe": [
                "The spirits whisper...",
                "My gods show me...",
                "The signs are clear...",
            ],
            "act": [
                "With warrior's grace...",
                "As my fathers taught...",
                "Following ancient ways...",
            ]
        }
    
    def process_command(self, command: str, location: str) -> CharacterResponse:
        if "LOOK" in command:
            prefix = random.choice(self.vocabulary["observe"])
            if location == "waterfront":
                return CharacterResponse(
                    f"{prefix} these Western ships, strange as they are, carry the same spirit "
                    "as my people's war canoes. The waves speak in all languages.",
                    special_insight="The bones of whales tell stories of battles yet to come.",
                    affected_themes=["nature", "fate"]
                )
        return CharacterResponse("I read the omens before deciding.")

class CharacterAPI:
    """Manages character-specific command processing"""
    
    def __init__(self):
        self.handlers = {
            "ISHMAEL": IshmaelHandler(),
            "QUEEQUEG": QueequegHandler(),
            # Add other character handlers as needed
        }
    
    def process_command(self, character_id: str, command: str, location: str) -> CharacterResponse:
        """Process command through the appropriate character handler"""
        handler = self.handlers.get(character_id)
        if not handler:
            return CharacterResponse("Character not found.")
        return handler.process_command(command, location)
