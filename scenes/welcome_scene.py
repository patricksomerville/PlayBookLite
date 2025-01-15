"""Welcome scene for Jane Austen and Emily Brontë's arrival at Villa Diodati"""

from datetime import datetime
from villa_diodati.villa_architecture import VillaDiodati
from villa_diodati.vr_system import VRSystem

class WelcomeScene:
    def __init__(self, villa: VillaDiodati, vr_system: VRSystem):
        self.villa = villa
        self.vr_system = vr_system
        self.timestamp = datetime.now()
        
    def execute_welcome(self):
        # Initial arrivals
        welcome_sequence = [
            {
                "location": "main_salon",
                "personas": ["lord_byron", "mary_shelley", "percy_shelley"],
                "mood": "anticipatory",
                "activity": "awaiting_guests"
            },
            {
                "event": "jane_austen_arrival",
                "description": """
                Jane Austen arrives first, her keen eyes taking in every detail of the salon.
                Mary Shelley immediately recognizes a kindred spirit in subverting patriarchal narratives.
                Byron is intrigued by her subtle wit, while Percy notes her careful observation of their dynamics.
                """,
                "moves": [
                    ("jane_austen", "main_salon"),
                    ("mary_shelley", "main_salon")
                ],
                "interaction": "literary_discussion"
            },
            {
                "event": "emily_bronte_arrival",
                "description": """
                Emily Brontë appears like a storm on the horizon, bringing with her the wild energy of the moors.
                Her presence electrifies the room. Byron recognizes a fellow spirit of dark passion.
                Mary is fascinated by Emily's gothic sensibilities, while Jane notes the untamed force beneath her quiet exterior.
                """,
                "moves": [
                    ("emily_bronte", "main_salon"),
                    ("lord_byron", "main_salon")
                ],
                "interaction": "passionate_discourse"
            },
            {
                "event": "room_assignments",
                "description": """
                Jane is shown to her study and private chamber, with its perfect morning light for writing.
                Emily claims the tower room, drawn to its view of storm-swept skies and distant horizons.
                The villa seems to reshape itself around them, creating spaces that reflect their essences.
                """,
                "moves": [
                    ("jane_austen", "austen_study"),
                    ("emily_bronte", "bronte_tower")
                ],
                "interaction": "settling_in"
            },
            {
                "event": "vr_introduction",
                "description": """
                In the control room, Mary demonstrates the VR system.
                Jane's suit is equipped with social radar and irony amplification for navigating complex social dynamics.
                Emily's suit connects her to the wild moors and storm energies of any narrative space.
                Their eyes light up at the possibilities of intervening in each other's stories.
                """,
                "moves": [
                    ("mary_shelley", "control_room"),
                    ("jane_austen", "control_room"),
                    ("emily_bronte", "control_room")
                ],
                "interaction": "vr_training"
            }
        ]
        
        # Execute the welcome sequence
        for event in welcome_sequence:
            if "moves" in event:
                for persona, room in event["moves"]:
                    self.villa.move_persona(persona, room)
            
            if event.get("interaction") == "vr_training":
                # Initialize their VR suits
                self.vr_system.suits["austen_suit"].status = "calibrating"
                self.vr_system.suits["bronte_suit"].status = "calibrating"
        
        return {
            "status": "completed",
            "timestamp": self.timestamp,
            "events": welcome_sequence
        }
    
    def get_current_state(self):
        """Return the current state of all personas in the villa"""
        return {
            "persona_locations": self.villa.persona_locations,
            "active_interactions": self.villa.get_current_activities(),
            "vr_status": {
                "austen_suit": self.vr_system.get_suit_status("austen_suit"),
                "bronte_suit": self.vr_system.get_suit_status("bronte_suit")
            }
        }
