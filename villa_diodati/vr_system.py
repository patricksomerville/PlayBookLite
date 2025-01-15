"""VR System for literary personas to interact with their novels."""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import enum

class VRSuitStatus(enum.Enum):
    AVAILABLE = "available"
    IN_USE = "in_use"
    CHARGING = "charging"
    MAINTENANCE = "maintenance"

class MissionType(enum.Enum):
    STORY_INTERVENTION = "story_intervention"  # Direct interaction with story events
    CHARACTER_COUNSEL = "character_counsel"    # Advising characters
    WORLD_BUILDING = "world_building"         # Modifying story environment
    CRISIS_MANAGEMENT = "crisis_management"   # Handling story emergencies

@dataclass
class VRSuit:
    id: str
    assigned_to: Optional[str]
    status: VRSuitStatus
    charge_level: int
    last_maintenance: datetime
    special_features: List[str]

class VRSystem:
    """Manages the VR system for literary interventions."""
    
    def __init__(self):
        # Initialize VR suits
        self.suits: Dict[str, VRSuit] = {
            "byron_suit": VRSuit(
                id="byron_suit",
                assigned_to=None,
                status=VRSuitStatus.AVAILABLE,
                charge_level=100,
                last_maintenance=datetime.now(),
                special_features=["gothic_enhancement", "poetic_vision"]
            ),
            "mary_suit": VRSuit(
                id="mary_suit",
                assigned_to=None,
                status=VRSuitStatus.AVAILABLE,
                charge_level=100,
                last_maintenance=datetime.now(),
                special_features=["horror_sense", "scientific_overlay"]
            ),
            "percy_suit": VRSuit(
                id="percy_suit",
                assigned_to=None,
                status=VRSuitStatus.AVAILABLE,
                charge_level=100,
                last_maintenance=datetime.now(),
                special_features=["nature_attunement", "revolutionary_spirit"]
            ),
            "melville_suit": VRSuit(
                id="melville_suit",
                assigned_to=None,
                status=VRSuitStatus.AVAILABLE,
                charge_level=100,
                last_maintenance=datetime.now(),
                special_features=["maritime_sensors", "depth_perception"]
            ),
            "austen_suit": VRSuit(
                id="austen_suit",
                assigned_to=None,
                status=VRSuitStatus.AVAILABLE,
                charge_level=100,
                last_maintenance=datetime.now(),
                special_features=["social_radar", "irony_amplifier", "hidden_desire_detector"]
            ),
            "bronte_suit": VRSuit(
                id="bronte_suit",
                assigned_to=None,
                status=VRSuitStatus.AVAILABLE,
                charge_level=100,
                last_maintenance=datetime.now(),
                special_features=["moor_connection", "storm_sense", "passion_intensifier"]
            )
        }
        
        # Track active missions
        self.active_missions: Dict[str, Dict] = {}
        
        # Define novel-specific environments
        self.novel_environments = {
            "frankenstein": {
                "locations": ["laboratory", "arctic", "university", "swiss_alps"],
                "key_scenes": ["creation", "wedding", "arctic_pursuit"],
                "emergency_protocols": ["creature_containment", "igor_backup"]
            },
            "moby_dick": {
                "locations": ["pequod", "whaling_grounds", "sea_depths"],
                "key_scenes": ["first_sighting", "final_chase", "storm_sequence"],
                "emergency_protocols": ["whale_encounter", "ship_damage"]
            },
            "prometheus_unbound": {
                "locations": ["mountain_peak", "spirit_realm", "earth_cave"],
                "key_scenes": ["prometheus_bound", "asia_transformation"],
                "emergency_protocols": ["spirit_containment", "reality_stabilization"]
            },
            "pride_and_prejudice": {
                "locations": ["longbourn", "pemberley", "meryton", "netherfield"],
                "key_scenes": ["first_proposal", "pemberley_visit", "lydia_crisis"],
                "emergency_protocols": ["reputation_management", "marriage_intervention"]
            },
            "emma": {
                "locations": ["hartfield", "highbury", "box_hill", "donwell_abbey"],
                "key_scenes": ["emma_harriet_portrait", "box_hill_incident", "secret_engagement"],
                "emergency_protocols": ["matchmaking_crisis", "social_disaster"]
            },
            "wuthering_heights": {
                "locations": ["heights", "thrushcross_grange", "moors", "ghost_realm"],
                "key_scenes": ["catherine_ghost", "heathcliff_return", "young_cathy_escape"],
                "emergency_protocols": ["passion_overflow", "ghost_manifestation", "moor_storm"]
            }
        }
    
    def suit_up(self, persona: str) -> Dict:
        """Assign and prepare a VR suit for a persona."""
        suit_id = f"{persona.split('_')[0]}_suit"
        if suit_id not in self.suits:
            return {"status": "error", "message": f"No suit configured for {persona}"}
            
        suit = self.suits[suit_id]
        if suit.status != VRSuitStatus.AVAILABLE:
            return {"status": "error", "message": f"Suit {suit_id} not available"}
            
        suit.assigned_to = persona
        suit.status = VRSuitStatus.IN_USE
        
        return {
            "status": "success",
            "suit_id": suit_id,
            "features": suit.special_features,
            "charge": suit.charge_level
        }
    
    def start_mission(self, 
                     mission_name: str,
                     novel: str,
                     mission_type: MissionType,
                     participants: List[str]) -> Dict:
        """Initialize a VR mission into a novel."""
        if novel not in self.novel_environments:
            return {"status": "error", "message": f"Novel environment {novel} not configured"}
            
        # Suit up all participants
        suited_participants = []
        for persona in participants:
            suit_result = self.suit_up(persona)
            if suit_result["status"] == "error":
                return suit_result
            suited_participants.append({
                "persona": persona,
                "suit": suit_result["suit_id"]
            })
        
        # Create mission instance
        mission = {
            "name": mission_name,
            "novel": novel,
            "type": mission_type,
            "participants": suited_participants,
            "start_time": datetime.now(),
            "status": "active",
            "current_location": self.novel_environments[novel]["locations"][0]
        }
        
        self.active_missions[mission_name] = mission
        
        return {
            "status": "success",
            "mission": mission_name,
            "environment": self.novel_environments[novel],
            "suited_participants": suited_participants
        }
    
    def emergency_alert(self, novel: str, scene: str) -> Dict:
        """Handle emergency alerts from novels requiring intervention."""
        if novel not in self.novel_environments:
            return {"status": "error", "message": f"Novel {novel} not configured"}
            
        # Find available personas
        available_suits = [
            suit_id for suit_id, suit in self.suits.items()
            if suit.status == VRSuitStatus.AVAILABLE
        ]
        
        if not available_suits:
            return {"status": "error", "message": "No suits available for emergency response"}
            
        # Prepare emergency protocols
        protocols = self.novel_environments[novel]["emergency_protocols"]
        
        return {
            "status": "success",
            "alert_type": "emergency",
            "novel": novel,
            "scene": scene,
            "available_suits": available_suits,
            "protocols": protocols,
            "priority": "high"
        }
    
    def end_mission(self, mission_name: str) -> Dict:
        """End a VR mission and process results."""
        if mission_name not in self.active_missions:
            return {"status": "error", "message": f"Mission {mission_name} not found"}
            
        mission = self.active_missions[mission_name]
        
        # Release all suits
        for participant in mission["participants"]:
            suit = self.suits[participant["suit"]]
            suit.assigned_to = None
            suit.status = VRSuitStatus.CHARGING
            suit.charge_level = max(0, suit.charge_level - 20)  # Reduce charge
        
        # Archive mission data
        mission["end_time"] = datetime.now()
        mission["status"] = "completed"
        
        del self.active_missions[mission_name]
        
        return {
            "status": "success",
            "mission": mission_name,
            "duration": mission["end_time"] - mission["start_time"],
            "participants": [p["persona"] for p in mission["participants"]]
        }
    
    def get_suit_status(self, suit_id: str) -> Dict:
        """Get current status of a VR suit."""
        if suit_id not in self.suits:
            return {"status": "error", "message": f"Suit {suit_id} not found"}
            
        suit = self.suits[suit_id]
        return {
            "status": "success",
            "suit_id": suit_id,
            "assigned_to": suit.assigned_to,
            "condition": suit.status.value,
            "charge": suit.charge_level,
            "features": suit.special_features
        }
