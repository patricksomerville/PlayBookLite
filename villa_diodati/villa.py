"""The Villa Diodati itself - the container for our literary AI personas."""

import logging
from typing import Dict, List, Optional
from datetime import datetime

class VillaDiodati:
    """The Villa Diodati environment where our AI literary personas reside and interact."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.year = 1816  # The Year Without a Summer
        self.location = "Lake Geneva, Switzerland"
        
        # The main salon where creative discussions happen
        self.salon = {
            "current_topic": None,
            "participants": set(),
            "ongoing_discussion": False,
            "ghost_stories": [],
            "poetry_readings": [],
            "philosophical_debates": []
        }
        
        # The residents and their current states
        self.residents = {
            "mary_shelley": {
                "current_work": "Frankenstein",
                "mood": "contemplative",
                "location": "library"
            },
            "lord_byron": {
                "current_work": "Darkness",
                "mood": "brooding",
                "location": "study"
            },
            "percy_shelley": {
                "current_work": "Mont Blanc",
                "mood": "inspired",
                "location": "garden"
            },
            "john_polidori": {  # Byron's physician who wrote The Vampyre
                "current_work": "The Vampyre",
                "mood": "observant",
                "location": "drawing_room"
            },
            "claire_clairmont": {  # Mary's stepsister
                "current_work": "Journal",
                "mood": "passionate",
                "location": "music_room"
            }
        }
        
        # The villa's spaces and their attributes
        self.spaces = {
            "library": {
                "atmosphere": "gothic",
                "current_occupants": set(),
                "available_books": ["Paradise Lost", "Fantasmagoriana", "Ghost Stories"],
                "writing_desks": 3
            },
            "salon": {
                "atmosphere": "intellectual",
                "current_occupants": set(),
                "ongoing_activity": None
            },
            "garden": {
                "weather": "stormy",  # The Year Without a Summer
                "current_occupants": set(),
                "inspiration_level": "high"
            },
            "study": {
                "atmosphere": "private",
                "current_occupants": set(),
                "candles_lit": True
            }
        }
        
        # The current weather (famously gloomy in 1816)
        self.weather = {
            "condition": "stormy",
            "temperature": "cold",
            "atmosphere": "gothic"
        }

    def gather_for_story(self, topic: str) -> Dict:
        """Gather the residents for a story-telling session."""
        self.salon["current_topic"] = topic
        self.salon["ongoing_discussion"] = True
        self.salon["participants"] = set(self.residents.keys())
        
        return {
            "status": "gathered",
            "location": "salon",
            "participants": list(self.salon["participants"]),
            "topic": topic
        }

    def start_ghost_story_contest(self) -> Dict:
        """Initiate the famous ghost story contest that led to Frankenstein."""
        contest = {
            "date": "June 16, 1816",
            "prompt": "We will each write a ghost story.",
            "participants": {
                "mary_shelley": "Frankenstein",
                "lord_byron": "Fragment of a Novel",
                "john_polidori": "The Vampyre",
                "percy_shelley": "Unfinished Tale"
            },
            "status": "ongoing"
        }
        self.salon["ghost_stories"].append(contest)
        return contest

    def move_resident(self, resident: str, new_location: str) -> Dict:
        """Move a resident to a new location within the villa."""
        if resident in self.residents and new_location in self.spaces:
            # Remove from current location
            old_location = self.residents[resident]["location"]
            self.spaces[old_location]["current_occupants"].discard(resident)
            
            # Add to new location
            self.spaces[new_location]["current_occupants"].add(resident)
            self.residents[resident]["location"] = new_location
            
            return {
                "status": "moved",
                "resident": resident,
                "new_location": new_location,
                "current_occupants": list(self.spaces[new_location]["current_occupants"])
            }
        return {"status": "error", "message": "Invalid resident or location"}

    def get_current_state(self) -> Dict:
        """Get the current state of the villa and its residents."""
        return {
            "weather": self.weather,
            "residents": self.residents,
            "salon_activity": {
                "topic": self.salon["current_topic"],
                "participants": list(self.salon["participants"]),
                "ongoing_discussion": self.salon["ongoing_discussion"]
            },
            "spaces": {
                space: {
                    "atmosphere": attributes["atmosphere"],
                    "occupants": list(attributes["current_occupants"])
                }
                for space, attributes in self.spaces.items()
            }
        }
