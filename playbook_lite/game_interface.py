"""DOS-style text adventure interface for PlayBook."""

import os
import time
import sys
import re
from typing import Dict, List, Optional, Tuple, Set
from dataclasses import dataclass, field
from .story_state import StoryEngine
from .ascii_art import get_art

@dataclass
class Contribution:
    """A user's contribution to the story"""
    text: str
    location: str
    chapter: int
    themes: Set[str]
    affects_plot: bool = False
    referenced_characters: Set[str] = field(default_factory=set)

@dataclass
class Character:
    """A playable character in Moby Dick"""
    name: str
    description: str
    starting_location: str
    special_ability: str
    perspective: str

@dataclass
class GameState:
    """Tracks the current state of the text adventure"""
    current_location: str = "manhattan_streets"
    inventory: List[str] = field(default_factory=list)
    visited_locations: Set[str] = field(default_factory=set)
    current_chapter: int = 1
    story_engine: Optional[StoryEngine] = None
    last_command: Optional[str] = None
    user_contributions: List[Contribution] = field(default_factory=list)
    narrative_branches: Dict[str, List[str]] = field(default_factory=dict)
    active_themes: Set[str] = field(default_factory=lambda: {
        "isolation", "obsession", "nature", "fate", "identity"
    })
    selected_character: Optional[Character] = None

class TextInterface:
    """Handles DOS-style text adventure interface"""
    
    def __init__(self):
        self.story = StoryEngine()
        self.state = GameState(story_engine=self.story)
        self.key_characters = {
            "ISHMAEL", "QUEEQUEG", "AHAB", "STARBUCK", "MOBY DICK", "ELIJAH",
            "FEDALLAH", "PIP", "STUBB", "FLASK"
        }
        self.characters = {
            "ISHMAEL": Character(
                name="ISHMAEL",
                description="The philosophical observer. A schoolteacher seeking meaning on the seas.",
                starting_location="manhattan_streets",
                special_ability="CONTEMPLATE - Reveal deeper meanings in ordinary events",
                perspective="A thoughtful outsider's view of whaling life"
            ),
            "QUEEQUEG": Character(
                name="QUEEQUEG",
                description="The noble harpooner. A warrior-prince far from home.",
                starting_location="spouter_inn",
                special_ability="PROPHECY - Read omens in natural phenomena",
                perspective="A spiritual warrior's view of Western culture"
            ),
            "STARBUCK": Character(
                name="STARBUCK",
                description="The moral compass. First mate of the Pequod.",
                starting_location="pequod_deck",
                special_ability="REASON - Attempt to sway Ahab from his destructive path",
                perspective="A practical seaman's view of moral choice"
            ),
            "PIP": Character(
                name="PIP",
                description="The transformed cabin boy. Lost at sea, found something else.",
                starting_location="pequod_hold",
                special_ability="INSIGHT - Speak prophetic truths through seeming madness",
                perspective="An innocent's view of humanity's darkness"
            ),
            "MOBY": Character(
                name="MOBY",
                description="The great white whale. Nature's most mysterious creature.",
                starting_location="ocean_depths",
                special_ability="BREACH - Rise from the depths to confront your pursuers",
                perspective="The hunted becomes the hunter"
            )
        }
        
    def get_character_select_screen(self) -> str:
        """Generate the character selection screen"""
        output = []
        for name, char in self.characters.items():
            output.extend([
                f'Call me {name}',
                f'   {char.description}',
                f'   {char.special_ability}'
            ])
        return '\n'.join(output)

    def select_character(self, name: str) -> Dict[str, str]:
        """Handle character selection"""
        if name not in self.characters:
            return {
                "text": 'Please type "Call me" followed by a character name.',
                "ascii_art": None
            }
            
        character = self.characters[name]
        self.state.selected_character = character
        self.state.current_location = character.starting_location
        
        return {
            "text": f"""{character.perspective}
{character.special_ability}
The story begins...""",
            "ascii_art": get_art(character.name.lower())
        }

    def handle_command(self, command: str) -> Dict[str, str]:
        """Process a command and return the response"""
        command = command.upper()
        response = {"text": "", "ascii_art": None}
        
        if not self.state.selected_character:
            if command.startswith("CALL ME "):
                name = command[8:].strip()
                return self.select_character(name)
            elif command == "HELP":
                return {
                    "text": """ISHMAEL - The traditional narrator
QUEEQUEG - Experience the story from an "outsider's" perspective
STARBUCK - Witness the moral struggle against Ahab's obsession
PIP - See the world through transformed eyes
MOBY - Experience the hunt from the whale's perspective""",
                    "ascii_art": None
                }
            else:
                return {
                    "text": 'Type "Call me" followed by your chosen name.',
                    "ascii_art": None
                }
        
        if command == "HELP":
            response["text"] = self._get_help_text()
        elif command == "LOOK":
            response["text"] = self._look_around()
        elif command.startswith("GO "):
            direction = command[3:]
            response["text"] = self._move(direction)
        elif command == "INVENTORY":
            response["text"] = self._show_inventory()
        elif command.startswith("TALK "):
            person = command[5:]
            response["text"] = self._talk_to(person)
        elif command.startswith("WRITE "):
            contribution = command[6:]
            response["text"] = self._add_contribution(contribution)
        elif command == "READ":
            response["text"] = self._read_contributions()
        elif command == "THEMES":
            response["text"] = self._show_active_themes()
        else:
            response["text"] = "Unknown command. Type HELP for commands."
            
        self.state.last_command = command
        return response
        
    def _get_help_text(self) -> str:
        return """Available commands:
LOOK - Examine your surroundings
GO [DIRECTION] - Move in a direction (NORTH, SOUTH, EAST, WEST)
INVENTORY - Check your possessions
TALK [PERSON] - Speak with someone
WRITE [TEXT] - Add your own line to the story
READ - Review all contributed lines
THEMES - Show current story themes
HELP - Show this help text"""

    def _analyze_contribution(self, text: str) -> Tuple[Set[str], Set[str], bool]:
        """Analyze a contribution for themes, characters, and plot impact"""
        themes = set()
        characters = set()
        affects_plot = False
        
        # Check for character references
        for character in self.key_characters:
            if character in text.upper():
                characters.add(character)
                affects_plot = True  # Character mentions might affect plot
        
        # Theme detection
        theme_keywords = {
            "isolation": ["alone", "lonely", "solitude", "isolated", "single"],
            "obsession": ["hunt", "chase", "pursue", "revenge", "must", "will"],
            "nature": ["sea", "ocean", "whale", "wind", "storm", "waves"],
            "fate": ["destiny", "doom", "inevitable", "cursed", "written"],
            "identity": ["who", "self", "name", "call me", "soul", "spirit"]
        }
        
        for theme, keywords in theme_keywords.items():
            if any(word in text.lower() for word in keywords):
                themes.add(theme)
                
        # Check for potential plot impact
        plot_keywords = ["death", "kill", "change", "never", "forever", "oath", "promise"]
        if any(word in text.lower() for word in plot_keywords):
            affects_plot = True
            
        return themes, characters, affects_plot

    def _add_contribution(self, text: str) -> str:
        """Add a user's contribution to the story"""
        if not text:
            return "What would you like to write?"
            
        # Analyze the contribution
        themes, characters, affects_plot = self._analyze_contribution(text)
        
        # Create the contribution
        contribution = Contribution(
            text=text,
            location=self.state.current_location,
            chapter=self.state.current_chapter,
            themes=themes,
            affects_plot=affects_plot,
            referenced_characters=characters
        )
        
        self.state.user_contributions.append(contribution)
        
        # Update active themes
        if themes:
            self.state.active_themes.update(themes)
        
        # Generate response based on analysis
        response = [f'Your words have been added to the story:\n"{text}"\n']
        
        if themes:
            response.append(f"Themes detected: {', '.join(themes)}")
        
        if characters:
            response.append(f"Characters referenced: {', '.join(characters)}")
            
        if affects_plot:
            response.append("\nYour words may affect the course of the story...")
            
        response.append('\nAs Melville said, "It is better to fail in originality than to succeed in imitation."')
        
        return "\n".join(response)

    def _read_contributions(self) -> str:
        """Read all user contributions"""
        if not self.state.user_contributions:
            return "No lines have been written yet. Use WRITE to add your own."
            
        output = ["The story grows with each voice:\n"]
        
        for contrib in self.state.user_contributions:
            output.append(f'"{contrib.text}"')
            if contrib.themes:
                output.append(f"[Themes: {', '.join(contrib.themes)}]")
            output.append("")  # Empty line for spacing
            
        return "\n".join(output)

    def _show_active_themes(self) -> str:
        """Display currently active themes in the story"""
        return f"""Active themes in your version of Moby Dick:
{', '.join(self.state.active_themes)}

Your contributions can strengthen existing themes or introduce new ones."""

    def _look_around(self) -> str:
        if self.state.current_location == "manhattan_streets":
            return """The bustling streets of Manhattan surround you. The air is thick with coal smoke 
and the shouts of merchants. To the SOUTH lies the waterfront, where you might 
find passage on a whaling ship."""
        elif self.state.current_location == "waterfront":
            return """The docks stretch before you, a forest of masts and rigging. Ships of all sizes
bob in the harbor. The Pequod, a Nantucket whaler, catches your eye. 
The streets of Manhattan lie to the NORTH."""
        return "You find yourself in an unfamiliar place."

    def _move(self, direction: str) -> str:
        if direction == "SOUTH" and self.state.current_location == "manhattan_streets":
            self.state.current_location = "waterfront"
            return "You make your way down to the waterfront."
        elif direction == "NORTH" and self.state.current_location == "waterfront":
            self.state.current_location = "manhattan_streets"
            return "You return to the city streets."
        return "You cannot go that way."

    def _show_inventory(self) -> str:
        if not self.state.inventory:
            return "You are carrying nothing but a few coins and the clothes on your back."
        return "You are carrying:\n" + "\n".join(f"- {item}" for item in self.state.inventory)

    def _talk_to(self, person: str) -> str:
        if person == "QUEEQUEG" and self.state.current_location == "waterfront":
            return """The tattooed harpooner regards you with interest. "You looking for ship?" he asks
in broken English. "Pequod good ship. Captain Ahab, he great whale hunter."""
        return f"There is no one here by that name."
