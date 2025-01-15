"""Villa Diodati's physical and virtual architecture."""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from datetime import datetime
import enum

class RoomType(enum.Enum):
    HISTORICAL = "historical"  # Original Villa Diodati rooms
    VIRTUAL = "virtual"        # VR/Control room spaces

class ActivityType(enum.Enum):
    WRITING = "writing"
    READING = "reading"
    AFFAIR = "affair"
    CONVERSATION = "conversation"
    STORY_SHARING = "story_sharing"
    VR_MISSION = "vr_mission"
    RESTING = "resting"

@dataclass
class Room:
    name: str
    room_type: RoomType
    current_occupants: Set[str]
    max_occupants: int
    mood_lighting: str
    current_activity: Optional[ActivityType]
    private: bool
    connected_rooms: List[str]
    
    # For the Control Room
    vr_suits_available: Optional[int] = None
    active_mission: Optional[str] = None

class VillaDiodati:
    """Real-time management of Villa Diodati's physical and virtual spaces."""
    
    def __init__(self):
        # Initialize the villa's architecture
        self.rooms: Dict[str, Room] = {
            # Historical Spaces
            "main_salon": Room(
                name="Main Salon",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=8,
                mood_lighting="warm candlelight",
                current_activity=None,
                private=False,
                connected_rooms=["library", "dining_room", "garden_entrance", "austen_study"]
            ),
            "library": Room(
                name="Library",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=4,
                mood_lighting="soft lamp light",
                current_activity=None,
                private=False,
                connected_rooms=["main_salon", "byron_study"]
            ),
            "byron_study": Room(
                name="Byron's Study",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=3,
                mood_lighting="moody candlelight",
                current_activity=None,
                private=True,
                connected_rooms=["library", "byron_bedroom"]
            ),
            "mary_chamber": Room(
                name="Mary's Chamber",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=2,
                mood_lighting="ghostly moonlight",
                current_activity=None,
                private=True,
                connected_rooms=["percy_chamber", "upper_hall"]
            ),
            "percy_chamber": Room(
                name="Percy's Chamber",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=2,
                mood_lighting="storm lantern",
                current_activity=None,
                private=True,
                connected_rooms=["mary_chamber", "upper_hall"]
            ),
            "garden": Room(
                name="Garden",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=6,
                mood_lighting="natural",
                current_activity=None,
                private=False,
                connected_rooms=["garden_entrance", "lake_view"]
            ),
            "lake_view": Room(
                name="Lake View Terrace",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=4,
                mood_lighting="natural",
                current_activity=None,
                private=False,
                connected_rooms=["garden"]
            ),
            "austen_study": Room(
                name="Austen's Study",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=3,
                mood_lighting="morning sunlight",
                current_activity=None,
                private=True,
                connected_rooms=["main_salon", "austen_chamber", "conservatory"]
            ),
            "austen_chamber": Room(
                name="Austen's Private Chamber",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=2,
                mood_lighting="soft lamplight",
                current_activity=None,
                private=True,
                connected_rooms=["austen_study", "upper_hall"]
            ),
            "bronte_tower": Room(
                name="Brontë's Tower",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=2,
                mood_lighting="stormy twilight",
                current_activity=None,
                private=True,
                connected_rooms=["upper_hall", "tower_study"]
            ),
            "tower_study": Room(
                name="Tower Study",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=3,
                mood_lighting="wild moonlight",
                current_activity=None,
                private=True,
                connected_rooms=["bronte_tower", "tower_balcony"]
            ),
            "tower_balcony": Room(
                name="Tower Balcony",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=2,
                mood_lighting="natural",
                current_activity=None,
                private=True,
                connected_rooms=["tower_study"]
            ),
            "conservatory": Room(
                name="Conservatory",
                room_type=RoomType.HISTORICAL,
                current_occupants=set(),
                max_occupants=4,
                mood_lighting="filtered sunlight",
                current_activity=None,
                private=False,
                connected_rooms=["austen_study", "garden"]
            ),
            
            # Virtual/Control Spaces
            "control_room": Room(
                name="Control Room",
                room_type=RoomType.VIRTUAL,
                current_occupants=set(),
                max_occupants=6,
                mood_lighting="sci-fi blue",
                current_activity=None,
                private=True,
                connected_rooms=["vr_prep_chamber"],
                vr_suits_available=6,
                active_mission=None
            ),
            "vr_prep_chamber": Room(
                name="VR Preparation Chamber",
                room_type=RoomType.VIRTUAL,
                current_occupants=set(),
                max_occupants=6,
                mood_lighting="tech white",
                current_activity=None,
                private=True,
                connected_rooms=["control_room"],
                vr_suits_available=6
            )
        }
        
        # Track persona locations and activities
        self.persona_locations: Dict[str, str] = {}
        self.current_affairs: List[tuple] = []
        self.active_readings: Dict[str, List[str]] = {}
        self.vr_missions: Dict[str, List[str]] = {}
        
        # Initialize default locations
        self.persona_locations = {
            "lord_byron": "byron_study",
            "mary_shelley": "mary_chamber",
            "percy_shelley": "library",
            "herman_melville": "lake_view",
            "jane_austen": "austen_study",
            "emily_bronte": "bronte_tower"
        }
    
    def move_persona(self, persona: str, target_room: str) -> Dict:
        """Move a persona to a new room."""
        if target_room not in self.rooms:
            return {"status": "error", "message": f"Room {target_room} does not exist"}
            
        current_room = self.persona_locations.get(persona)
        if current_room:
            self.rooms[current_room].current_occupants.remove(persona)
            
        if len(self.rooms[target_room].current_occupants) >= self.rooms[target_room].max_occupants:
            return {"status": "error", "message": f"{target_room} is at maximum occupancy"}
            
        self.rooms[target_room].current_occupants.add(persona)
        self.persona_locations[persona] = target_room
        
        return {
            "status": "success",
            "persona": persona,
            "new_room": target_room,
            "occupants": list(self.rooms[target_room].current_occupants)
        }
    
    def start_activity(self, room: str, activity: ActivityType, participants: List[str]) -> Dict:
        """Start a new activity in a room."""
        if room not in self.rooms:
            return {"status": "error", "message": f"Room {room} does not exist"}
            
        if self.rooms[room].current_activity:
            return {"status": "error", "message": f"Room is busy with {self.rooms[room].current_activity}"}
            
        # Move all participants to the room
        for persona in participants:
            move_result = self.move_persona(persona, room)
            if move_result["status"] == "error":
                return move_result
                
        self.rooms[room].current_activity = activity
        
        if activity == ActivityType.AFFAIR:
            self.current_affairs.append(tuple(participants))
        elif activity == ActivityType.READING:
            self.active_readings[room] = participants
            
        return {
            "status": "success",
            "room": room,
            "activity": activity,
            "participants": participants
        }
    
    def trigger_vr_mission(self, mission_name: str, participants: List[str]) -> Dict:
        """Trigger a VR mission alert and move personas to Control Room."""
        # First, check if Control Room is available
        if self.rooms["control_room"].active_mission:
            return {"status": "error", "message": "Control Room already has active mission"}
            
        # Move participants to VR Prep Chamber
        for persona in participants:
            move_result = self.move_persona(persona, "vr_prep_chamber")
            if move_result["status"] == "error":
                return move_result
                
        # Start the mission
        self.rooms["control_room"].active_mission = mission_name
        self.vr_missions[mission_name] = participants
        
        return {
            "status": "success",
            "mission": mission_name,
            "participants": participants,
            "location": "vr_prep_chamber",
            "next_step": "suit_up"
        }
    
    def get_room_status(self, room: str) -> Dict:
        """Get current status of a room."""
        if room not in self.rooms:
            return {"status": "error", "message": f"Room {room} does not exist"}
            
        room_data = self.rooms[room]
        return {
            "status": "success",
            "name": room_data.name,
            "type": room_data.room_type.value,
            "occupants": list(room_data.current_occupants),
            "activity": room_data.current_activity.value if room_data.current_activity else None,
            "mood": room_data.mood_lighting,
            "connected_rooms": room_data.connected_rooms,
            "is_private": room_data.private
        }
    
    def get_persona_status(self, persona: str) -> Dict:
        """Get current status of a persona."""
        current_room = self.persona_locations.get(persona)
        if not current_room:
            return {"status": "error", "message": f"Persona {persona} not found"}
            
        current_activities = []
        if any(persona in affair for affair in self.current_affairs):
            current_activities.append("In an affair")
        if any(persona in readers for readers in self.active_readings.values()):
            current_activities.append("Participating in reading")
        if any(persona in mission for mission in self.vr_missions.values()):
            current_activities.append("On VR mission")
            
        return {
            "status": "success",
            "persona": persona,
            "location": current_room,
            "current_activities": current_activities,
            "room_occupants": list(self.rooms[current_room].current_occupants)
        }
