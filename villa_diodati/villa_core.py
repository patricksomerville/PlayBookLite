"""Core Villa Diodati architecture and room management"""

from typing import Dict, Set, List, Optional
from dataclasses import dataclass
from enum import Enum

class RoomType(Enum):
    HISTORICAL = "historical"
    VIRTUAL = "virtual"
    CONTROL = "control"

@dataclass
class Room:
    name: str
    room_type: RoomType
    current_occupants: Set[str]
    max_occupants: int
    mood_lighting: str
    current_activity: Optional[str]
    private: bool
    connected_rooms: List[str]

class VillaDiodati:
    """Manages the Villa Diodati architecture and persona movements"""
    
    def __init__(self):
        # Initialize default locations
        self.persona_locations = {
            "lord_byron": "byron_study",
            "mary_shelley": "mary_chamber",
            "percy_shelley": "library",
            "herman_melville": "lake_view",
            "jane_austen": "main_salon",
            "emily_bronte": "garden"
        }
        
        self.rooms = {
            # Historical Spaces
            "main_salon": Room(
                name="Main Salon",
                room_type=RoomType.HISTORICAL,
                current_occupants={"jane_austen"},
                max_occupants=8,
                mood_lighting="warm candlelight",
                current_activity=None,
                private=False,
                connected_rooms=["library", "dining_room", "garden_entrance"]
            ),
            "library": Room(
                name="Library",
                room_type=RoomType.HISTORICAL,
                current_occupants={"percy_shelley"},
                max_occupants=4,
                mood_lighting="soft lamplight",
                current_activity=None,
                private=False,
                connected_rooms=["main_salon", "study_corridor"]
            ),
            "garden": Room(
                name="Garden",
                room_type=RoomType.HISTORICAL,
                current_occupants={"emily_bronte"},
                max_occupants=10,
                mood_lighting="natural",
                current_activity=None,
                private=False,
                connected_rooms=["garden_entrance", "lake_view", "conservatory"]
            ),
            "lake_view": Room(
                name="Lake View",
                room_type=RoomType.HISTORICAL,
                current_occupants={"herman_melville"},
                max_occupants=3,
                mood_lighting="natural",
                current_activity=None,
                private=True,
                connected_rooms=["garden"]
            ),
            "byron_study": Room(
                name="Byron's Study",
                room_type=RoomType.HISTORICAL,
                current_occupants={"lord_byron"},
                max_occupants=2,
                mood_lighting="moody candlelight",
                current_activity=None,
                private=True,
                connected_rooms=["study_corridor", "byron_chamber"]
            ),
            "mary_chamber": Room(
                name="Mary's Chamber",
                room_type=RoomType.HISTORICAL,
                current_occupants={"mary_shelley"},
                max_occupants=2,
                mood_lighting="gothic shadows",
                current_activity=None,
                private=True,
                connected_rooms=["upper_hall", "mary_study"]
            ),
            "conservatory": Room(
                name="Conservatory",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=4,
                mood_lighting="filtered sunlight",
                current_activity=None,
                private=False,
                connected_rooms=["garden", "upper_hall"]
            ),
            "upper_hall": Room(
                name="Upper Hall",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=6,
                mood_lighting="dim candlelight",
                current_activity=None,
                private=False,
                connected_rooms=["mary_chamber", "byron_chamber", "conservatory", "study_corridor"]
            ),
            "study_corridor": Room(
                name="Study Corridor",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=4,
                mood_lighting="flickering shadows",
                current_activity=None,
                private=False,
                connected_rooms=["library", "byron_study", "upper_hall"]
            ),
            "garden_entrance": Room(
                name="Garden Entrance",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=4,
                mood_lighting="natural",
                current_activity=None,
                private=False,
                connected_rooms=["main_salon", "garden"]
            )
        }
    
    def move_persona(self, persona: str, target_room: str) -> Dict:
        """Move a persona to a new room"""
        if target_room not in self.rooms:
            return {"status": "error", "message": f"Room {target_room} does not exist"}
        
        if len(self.rooms[target_room].current_occupants) >= self.rooms[target_room].max_occupants:
            return {"status": "error", "message": f"Room {target_room} is at maximum capacity"}
        
        # Remove from current room
        current_room = self.persona_locations[persona]
        self.rooms[current_room].current_occupants.remove(persona)
        
        # Add to new room
        self.rooms[target_room].current_occupants.add(persona)
        self.persona_locations[persona] = target_room
        
        return {
            "status": "success",
            "persona": persona,
            "from_room": current_room,
            "to_room": target_room
        }
    
    def get_current_activities(self) -> Dict[str, List[str]]:
        """Get all current activities and their participants"""
        activities = {}
        for room_id, room in self.rooms.items():
            if room.current_activity:
                activities[room_id] = {
                    "activity": room.current_activity,
                    "participants": list(room.current_occupants)
                }
        return activities
