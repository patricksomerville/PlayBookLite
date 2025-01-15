"""A playful game of tag between the literary personas in Villa Diodati"""

from datetime import datetime
from typing import Dict, List, Set
import random
from villa_diodati.villa_core import VillaDiodati

class TagGame:
    def __init__(self, villa: VillaDiodati):
        self.villa = villa
        self.timestamp = datetime.now()
        self.it_persona = None
        self.game_log = []
        self.safe_zones = {"library", "control_room"}  # Can only stay 30 seconds
        self.safe_zone_timers = {}
        
    def start_game(self) -> Dict:
        """Initialize the game of tag"""
        # Everyone starts in the garden
        players = ["lord_byron", "mary_shelley", "percy_shelley", 
                  "jane_austen", "emily_bronte", "herman_melville"]
        
        for player in players:
            self.villa.move_persona(player, "garden")
        
        # Byron volunteers to be "it" first
        self.it_persona = "lord_byron"
        
        self.log_event(f"Lord Byron, with a mischievous grin, declares himself 'it' and gives everyone a 30-second head start.")
        return self.get_game_state()
    
    def log_event(self, event: str):
        """Record a game event"""
        self.game_log.append({
            "timestamp": datetime.now(),
            "event": event
        })
    
    def get_available_moves(self, persona: str) -> List[str]:
        """Get possible rooms a persona can move to"""
        current_room = self.villa.persona_locations[persona]
        return self.villa.rooms[current_room].connected_rooms
    
    def choose_strategic_move(self, persona: str) -> str:
        """Choose a strategic move based on persona's personality"""
        available_rooms = self.get_available_moves(persona)
        current_room = self.villa.persona_locations[persona]
        it_location = self.villa.persona_locations[self.it_persona]
        
        if persona == self.it_persona:
            # If "it", try to move towards the nearest player
            target_locations = [self.villa.persona_locations[p] for p in self.villa.persona_locations 
                              if p != self.it_persona]
            # Simple strategy: move to a room that's occupied if possible
            for room in available_rooms:
                if room in target_locations:
                    return room
        else:
            # If not "it", try to move away from "it"
            if it_location in available_rooms:
                # If "it" is in an adjacent room, definitely move away
                available_rooms.remove(it_location)
            
            # Consider personality-based strategies
            if persona == "emily_bronte":
                # Emily might hide in the tower or dark corners
                for room in ["bronte_tower", "tower_study", "tower_balcony"]:
                    if room in available_rooms:
                        return room
            
            elif persona == "jane_austen":
                # Jane might prefer social spaces where she can observe
                for room in ["conservatory", "main_salon"]:
                    if room in available_rooms:
                        return room
            
            elif persona == "mary_shelley":
                # Mary might use the villa's secret passages
                for room in ["mary_chamber", "control_room"]:
                    if room in available_rooms:
                        return room
        
        # If no strategic preference, choose randomly
        return random.choice(available_rooms) if available_rooms else current_room
    
    def generate_chase_narrative(self, chaser: str, target: str, from_room: str, to_room: str) -> str:
        """Generate a narrative description of a chase"""
        narratives = {
            "lord_byron": {
                "style": "dramatic and poetic",
                "moves": ["swiftly glides", "dashes with romantic flair", "pursues with poetic grace"]
            },
            "mary_shelley": {
                "style": "gothic and mysterious",
                "moves": ["slips through shadows", "navigates the darkness", "moves like a phantom"]
            },
            "emily_bronte": {
                "style": "wild and passionate",
                "moves": ["races like the wind", "moves with untamed grace", "darts like a storm"]
            },
            "jane_austen": {
                "style": "precise and observant",
                "moves": ["strategically advances", "moves with calculated grace", "proceeds with wit"]
            },
            "herman_melville": {
                "style": "adventurous and determined",
                "moves": ["pursues like a seasoned captain", "navigates the space", "charts a course"]
            },
            "percy_shelley": {
                "style": "ethereal and swift",
                "moves": ["floats like spirit", "moves like lightning", "dances through space"]
            }
        }
        
        chaser_style = narratives[chaser]
        move = random.choice(chaser_style["moves"])
        return f"{chaser.replace('_', ' ').title()} {move} from {from_room.replace('_', ' ')} to {to_room.replace('_', ' ')}"
    
    def play_round(self) -> Dict:
        """Play one round of the game"""
        # First move the person who's "it"
        it_current_room = self.villa.persona_locations[self.it_persona]
        it_new_room = self.choose_strategic_move(self.it_persona)
        self.villa.move_persona(self.it_persona, it_new_room)
        
        # Log the chase
        self.log_event(self.generate_chase_narrative(
            self.it_persona, None, it_current_room, it_new_room
        ))
        
        # Then move other personas
        for persona in self.villa.persona_locations:
            if persona != self.it_persona:
                current_room = self.villa.persona_locations[persona]
                new_room = self.choose_strategic_move(persona)
                
                if current_room != new_room:
                    self.villa.move_persona(persona, new_room)
                    if random.random() < 0.3:  # Only log some movements for brevity
                        self.log_event(self.generate_chase_narrative(
                            persona, None, current_room, new_room
                        ))
        
        # Check for tags
        it_room = self.villa.persona_locations[self.it_persona]
        for persona in self.villa.persona_locations:
            if (persona != self.it_persona and 
                self.villa.persona_locations[persona] == it_room and
                it_room not in self.safe_zones):
                # Tag!
                old_it = self.it_persona
                self.it_persona = persona
                self.log_event(f"{old_it.replace('_', ' ').title()} tagged {persona.replace('_', ' ').title()}! The game continues with new pursuit...")
                break
        
        return self.get_game_state()
    
    def get_game_state(self) -> Dict:
        """Return the current state of the game"""
        return {
            "it_persona": self.it_persona,
            "locations": self.villa.persona_locations,
            "game_log": self.game_log[-5:],  # Last 5 events
            "timestamp": datetime.now()
        }
