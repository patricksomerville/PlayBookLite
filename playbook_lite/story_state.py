from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging
from .ascii_art import get_art

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@dataclass
class StoryBranch:
    """Tracks divergences from canonical Moby Dick text and manages narrative tension"""
    branch_id: str
    divergence_point: str
    canonical_action: 'CharacterAction'
    alternate_action: 'CharacterAction'
    consequences: List[str]
    thematic_consistency: float  # 0-1 scale of alignment with themes
    character_impacts: Dict[str, Dict[str, Any]]
    is_point_of_no_return: bool = False
    alternate_ending_required: bool = False
    thematic_elements: Dict[str, float] = field(default_factory=dict)
    narrative_tension: float = 0.0

    def evaluate_narrative_tension(self) -> Dict[str, float]:
        """
        Calculate how this branch creates tension between player freedom 
        and canonical story elements
        """
        tensions = {
            'thematic': 1.0 - self.thematic_consistency,
            'character': sum(
                impact.get('severity', 0.0) 
                for impact in self.character_impacts.values()
            ) / len(self.character_impacts) if self.character_impacts else 0.0,
            'plot': 0.8 if self.is_point_of_no_return else 0.4
        }

        # Calculate overall narrative tension
        self.narrative_tension = sum(tensions.values()) / len(tensions)
        return tensions

    def get_player_warning(self) -> str:
        """Generate appropriate warning about story divergence"""
        if self.is_point_of_no_return:
            return (
                "Your choices have led to a significant departure from Melville's text. "
                "While the themes of obsession, fate, and humanity's relationship with "
                "nature remain, your story will now forge its own unique path. The "
                "ending you discover will be different from the canonical text."
            )
        elif self.narrative_tension > 0.7:
            return (
                "Your story is beginning to diverge significantly from the original. "
                "While a return to the canonical path is still possible, your choices "
                "are shaping a unique interpretation of Moby Dick."
            )
        return (
            "Your choices represent a slight departure from the original text, "
            "offering a fresh perspective while maintaining the core narrative."
        )

@dataclass
class CharacterAction:
    """
    Represents a specific action taken by a character that causally impacts story events.
    An action must either be:
    1. A verbal statement/declaration that changes other characters' behavior or knowledge
       - Can be a single impactful sentence
       - Must have clear intention and consequence
       - Changes other characters' understanding or behavior
    2. A physical action that directly affects the story's progression
    """
    character_id: str
    action_type: str  # "verbal" or "physical"
    description: str  # Keep under 50 words, focus on the action itself
    direct_impact: str  # Immediate consequence of this action
    causal_chain: List[str]  # Series of events this action triggers
    influenced_characters: Dict[str, str]  # How other characters are affected
    timestamp: datetime
    location: str
    witnesses: List[str]  # Other characters present
    story_significance: float  # 0-1 scale of how crucial this action is to plot
    player_choices: Dict[str, Dict[str, Any]]  # Ways to interpret/react to action
    knowledge_requirements: Dict[str, bool]  # What characters need to know to understand
    agency_points: List[Dict[str, Any]]  # Specific moments where player can influence outcome
    canonical_text_reference: str  # Direct quote from Moby Dick showing this action
    intention: Optional[str] = None  # For verbal actions: the speaker's intent
    response_options: Optional[Dict[str, str]] = None  # Possible ways other characters can respond
    dialogue_context: Optional[Dict[str, Any]] = None  # Previous statements this responds to
    emotional_impact: Optional[Dict[str, float]] = None  # How this affects emotional states
    verbal_style: Optional[str] = None  # The manner of speaking (commanding, questioning, etc.)
    is_canonical: bool = True  # Whether this action occurs in the original text
    alternate_options: List[Dict[str, Any]] = field(default_factory=list)  # Player-available alternatives

@dataclass
class CharacterTimeline:
    """Tracks a character's significant actions through the story"""
    character_id: str
    core_actions: List[CharacterAction]  # Canon actions from the text that impact plot
    optional_actions: List[CharacterAction]  # Player-influenced possibilities
    relationship_states: Dict[str, float]  # Current standing with other characters
    knowledge_state: Dict[str, bool]  # What this character knows
    decision_points: List[Dict[str, Any]]  # Where player choices matter most
    action_consequences: Dict[str, List[str]]  # Track how each action affects later events
    story_branches: List[StoryBranch] = field(default_factory=list)  # Track divergences from canon

    def get_available_actions(self, current_state: Dict[str, Any]) -> List[CharacterAction]:
        """Get actions available based on current state and knowledge"""
        available = []
        for action in self.core_actions + self.optional_actions:
            if self._meets_requirements(action, current_state):
                # Check if this action makes causal sense given the current state
                if self._is_causally_valid(action, current_state):
                    available.append(action)
        return available

    def _meets_requirements(self, action: CharacterAction, state: Dict[str, Any]) -> bool:
        """Check if an action is available given current state"""
        # Check knowledge requirements
        for knowledge, required in action.knowledge_requirements.items():
            if state.get(f"knows_{knowledge}", False) != required:
                return False
        return True

    def _is_causally_valid(self, action: CharacterAction, state: Dict[str, Any]) -> bool:
        """Verify if this action makes sense in the causal chain"""
        # Check if prerequisite events have occurred
        if action.action_type == "verbal":
            # Character must be present and able to speak
            if not state.get("can_speak", True):
                return False
        elif action.action_type == "physical":
            # Character must be physically capable and in position
            if not state.get("can_act", True):
                return False
        return True

    def create_story_branch(self, canonical_action: CharacterAction, player_choice: Dict[str, Any]) -> StoryBranch:
        """Create a new story branch when player deviates from canon"""
        alternate_action = CharacterAction(
            character_id=canonical_action.character_id,
            action_type=player_choice["action_type"],
            description=player_choice["description"],
            direct_impact=player_choice["impact"],
            causal_chain=[],  # To be generated by AI
            influenced_characters={},  # To be generated by AI
            timestamp=datetime.now(),
            location=canonical_action.location,
            witnesses=canonical_action.witnesses,
            story_significance=canonical_action.story_significance,
            player_choices={},
            knowledge_requirements=canonical_action.knowledge_requirements,
            agency_points=[],
            canonical_text_reference="",
            is_canonical=False
        )

        branch = StoryBranch(
            branch_id=f"branch_{len(self.story_branches) + 1}",
            divergence_point=canonical_action.canonical_text_reference,
            canonical_action=canonical_action,
            alternate_action=alternate_action,
            consequences=[],  # To be generated by AI
            thematic_consistency=0.0,  # To be calculated
            character_impacts={}  # To be generated by AI
        )

        self.story_branches.append(branch)
        return branch

@dataclass
class CharacterPosition:
    """Tracks a character's precise location and state at a plot point"""
    character_id: str
    physical_location: str  # Specific location (e.g. "forecastle", "quarter-deck")
    ship_deck_level: Optional[str]  # For when on the Pequod
    proximity_to_others: Dict[str, float]  # Distance to other characters (0-1)
    is_present: bool  # Whether they're actually in the scene
    status: str  # Current activity or state
    accessibility: Dict[str, bool]  # Who can interact with them

@dataclass
class PlotEvent:
    """Represents an objective event in the story's reality"""
    id: str
    timestamp: datetime
    location: str
    description: str
    participating_characters: List[str]
    physical_effects: Dict[str, Any]  # Measurable changes in the story world
    canonical_reference: str  # Reference to the original text
    visual_description: str  # For AI art generation
    emotional_tone: Dict[str, float]  # Emotional mapping for music/atmosphere

@dataclass
class CharacterPerception:
    """How a character interprets and experiences events"""
    character_id: str
    plot_event_id: str
    interpretation: str  # Their understanding of what happened
    emotional_response: Dict[str, float]  # Emotional reactions with intensity
    knowledge_state: Dict[str, bool]  # What they know/don't know
    sensory_details: Dict[str, str]  # What they perceive through senses
    misconceptions: Dict[str, str]  # False beliefs about the event
    memory_links: List[str]  # Connections to past experiences
    inner_monologue: str  # Character's thoughts
    decision_factors: Dict[str, float]  # Influences on their choices

@dataclass
class StoryChoice:
    """Represents a choice available to the character"""
    id: str
    text: str
    requirements: Dict[str, Any]  # Required states/items/knowledge
    consequences: Dict[str, Any]  # Effects on story state
    emotional_weight: Dict[str, float]  # Emotional impact
    available_to: List[str]  # Characters who can make this choice
    narrative_weight: float  # Impact on overall story

@dataclass
class PlotPoint:
    """Canonical representation of a key moment in Moby Dick"""
    id: str
    chapter: int
    title: str
    location: str
    description: str  # Limited to 250 words
    narrative_tone: str
    character_timelines: Dict[str, CharacterTimeline]
    literary_devices: List[str]
    themes: List[str]
    symbols: Dict[str, str]
    historical_context: str
    weather_conditions: Dict[str, Any]
    time_of_day: str
    nautical_details: Dict[str, Any]
    canonical_text_reference: str
    calendar_date: Optional[str] = None
    character_positions: Dict[str, CharacterPosition] = field(default_factory=dict)

    def initialize_character_positions(self):
        """Initialize positions for all characters in timelines"""
        for char_id in self.character_timelines.keys():
            if char_id not in self.character_positions:
                self.character_positions[char_id] = CharacterPosition(
                    character_id=char_id,
                    physical_location=self.location,
                    ship_deck_level=None,
                    proximity_to_others={},
                    is_present=True,
                    status="active",
                    accessibility={}
                )

@dataclass
class StoryState:
    """Complete state combining objective plot and subjective perceptions"""
    id: str
    current_plot_event: PlotEvent
    character_perceptions: Dict[str, CharacterPerception]
    available_choices: List[StoryChoice]
    story_variables: Dict[str, Any]  # Track story-specific variables
    narrative_themes: List[str]  # Current active themes
    atmosphere: Dict[str, float]  # Environmental factors
    is_ending: bool = False

@dataclass
class IshmaelState:
    """Tracks Ishmael's progression through the narrative"""
    knowledge_of_whaling: float  # 0-1 scale of whaling expertise
    relationship_with_queequeg: float  # -1 to 1 relationship scale
    understanding_of_ahab: float  # 0-1 scale of insight into Ahab
    philosophical_depth: float  # 0-1 scale of existential understanding
    isolation_level: float  # 0-1 scale of detachment
    nautical_skill: float  # 0-1 scale of seamanship
    narrative_voice: float  # 0-1 scale of storytelling confidence
    physical_condition: float  # 0-1 scale of health/fatigue
    spiritual_awareness: float  # 0-1 scale of metaphysical understanding

class StoryEngine:
    """Manages story state and progression"""
    def __init__(self):
        logger.info("Initializing StoryEngine")
        self.current_chapter = 1
        self.current_plot = None
        self.ishmael_state = IshmaelState(
            knowledge_of_whaling=0.1,
            relationship_with_queequeg=0.0,
            understanding_of_ahab=0.0,
            philosophical_depth=0.3,
            isolation_level=0.8,
            nautical_skill=0.2,
            narrative_voice=0.4,
            physical_condition=0.9,
            spiritual_awareness=0.3
        )
        self.plot_events: Dict[str, PlotPoint] = {}
        self.initialize_moby_dick_plot()
        self.history: List[Dict] = []
        self.story_variables: Dict[str, Any] = {}
        self.divergence_threshold = 0.8  # Point at which canonical ending becomes unlikely
        self.current_branch: Optional[StoryBranch] = None
        self.branch_history: List[StoryBranch] = []
        logger.info("StoryEngine initialized successfully")

    def initialize_moby_dick_plot(self):
        """Initialize key plot points with precise character positions"""
        self.plot_events["manhattan_departure"] = PlotPoint(
            id="manhattan_departure",
            chapter=1,
            title="Loomings",
            location="Manhattan",
            description="""You find yourself in Manhattan, your purse light and your mood dark. 
            The damp, drizzly November in your soul has driven you once again to the sea.""",
            narrative_tone="contemplative",
            literary_devices=["first_person_narrative", "metaphor", "pathetic fallacy"],
            themes=["isolation", "escape", "spiritual_quest", "man_vs_self"],
            symbols={"sea": "freedom and spiritual truth", "land": "society's constraints"},
            historical_context="1850s New England maritime culture",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "cold",
                "precipitation": "drizzle",
                "wind": "moderate",
                "visibility": "poor"
            },
            time_of_day="evening",
            calendar_date="November 1850",
            nautical_details={
                "tide": "falling",
                "moon_phase": "waning crescent"
            },
            canonical_text_reference="Call me Ishmael. Some years ago—never mind how long precisely...",
        )

        # Initialize character positions for the plot point
        self.plot_events["manhattan_departure"].initialize_character_positions()


        self.plot_events["spouter_inn_arrival"] = PlotPoint(
            id="spouter_inn_arrival",
            chapter=2,
            title="The Spouter-Inn",
            location="New Bedford",
            description="""You arrive in New Bedford, seeking passage to Nantucket. 
            The Spouter-Inn looms before you, its weather-beaten sign creaking in the winter wind.""",
            narrative_tone="observant",
            literary_devices=["detailed_description", "foreshadowing", "symbolism"],
            themes=["journey_begins", "stranger_in_strange_land", "cultural_encounter"],
            symbols={
                "spouter_inn": "gateway to maritime world",
                "winter": "harsh realities ahead",
                "weathered_sign": "aged wisdom of seafaring"
            },
            historical_context="Whaling industry's golden age, New Bedford prosperity",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "queequeg": CharacterTimeline(
                    character_id="queequeg",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "freezing",
                "precipitation": "light snow",
                "wind": "strong",
                "visibility": "fair"
            },
            time_of_day="night",
            calendar_date="December 1850",
            nautical_details={},
            canonical_text_reference="In this same New Bedford there stands a Whaleman's Chapel...",
        )
        self.plot_events["spouter_inn_arrival"].initialize_character_positions()

        self.plot_events["meeting_queequeg"] = PlotPoint(
            id="meeting_queequeg",
            chapter=3,
            title="The Spouter-Inn: Meeting Queequeg",
            location="New Bedford, Spouter-Inn",
            description="""In the dim candlelight of your shared room, you encounter your 
            unexpected bedfellow - a tattooed harpooner from the South Seas.""",
            narrative_tone="tense_to_accepting",
            literary_devices=["dramatic_irony", "character_revelation", "cultural_contrast"],
            themes=["prejudice_vs_acceptance", "friendship", "cultural_understanding"],
            symbols={
                "tattoos": "cultural identity and story",
                "tomahawk_pipe": "bridge between cultures",
                "shared_bed": "breaking down of barriers"
            },
            historical_context="19th century racial and cultural prejudices",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "queequeg": CharacterTimeline(
                    character_id="queequeg",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "cold",
                "indoor_warmth": "moderate",
                "candle_light": "dim"
            },
            time_of_day="late_night",
            calendar_date="December 1850",
            nautical_details={},
            canonical_text_reference="Upon waking next morning about daylight, I found Queequeg's arm thrown over me...",
        )
        self.plot_events["meeting_queequeg"].initialize_character_positions()

        self.plot_events["whalemans_chapel"] = PlotPoint(
            id="whalemans_chapel",
            chapter=9,
            title="Father Mapple's Sermon",
            location="New Bedford, Whaleman's Chapel",
            description="""In the Whaleman's Chapel, Father Mapple ascends his pulpit-ladder 
            to deliver his powerful sermon on Jonah and the Whale, setting the spiritual tone 
            for the voyage ahead.""",
            narrative_tone="prophetic",
            literary_devices=["allegory", "foreshadowing", "biblical_parallel"],
            themes=["divine_will", "submission", "prophecy", "salvation"],
            symbols={
                "pulpit_ladder": "ascension to spiritual heights",
                "jonah": "defiance and submission to divine will",
                "whale": "instrument of divine purpose",
                "ship_pulpit": "authority and isolation"
            },
            historical_context="New England Protestant tradition and maritime spirituality",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "queequeg": CharacterTimeline(
                    character_id="queequeg",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "father_mapple": CharacterTimeline(
                    character_id="father_mapple",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "cold",
                "precipitation": "none",
                "indoor_atmosphere": "solemn",
                "lighting": "dim_candlelight"
            },
            time_of_day="morning",
            calendar_date="December 1850",
            nautical_details={},
            canonical_text_reference="With much interest I sat watching him. Though neither knew the other, Queequeg and I had gone to bed, in a fashion, as man and wife...",
        )
        self.plot_events["whalemans_chapel"].initialize_character_positions()

        self.plot_events["signing_pequod"] = PlotPoint(
            id="signing_pequod",
            chapter=16,
            title="Signing Aboard the Pequod",
            location="Nantucket, Spouter-Inn",
            description="""Captain Peleg and Captain Bildad interview Ishmael for service 
            aboard the Pequod, while the mysterious absence of Captain Ahab looms over 
            the proceedings.""",
            narrative_tone="ominous",
            literary_devices=["dramatic_irony", "foreshadowing", "mystery"],
            themes=["fate", "contract_with_destiny", "deception"],
            symbols={
                "contract": "binding with fate",
                "absent_captain": "hidden truth",
                "lay": "price of adventure",
                "owners_demeanor": "worldly wisdom vs spiritual concerns"
            },
            historical_context="Whaling industry contracts and hierarchy",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "peleg": CharacterTimeline(
                    character_id="peleg",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "bildad": CharacterTimeline(
                    character_id="bildad",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "cold",
                "wind": "strong",
                "indoor_warmth": "moderate"
            },
            time_of_day="morning",
            calendar_date="December 1850",
            nautical_details={
                "ship_condition": "docked",
                "tide": "rising"
            },
            canonical_text_reference="It was now clear sunrise. Soon after, Queequeg and I went up to the deck...",
        )
        self.plot_events["signing_pequod"].initialize_character_positions()

        self.plot_events["first_sight_pequod"] = PlotPoint(
            id="first_sight_pequod",
            chapter=20,
            title="First Sight of the Pequod",
            location="Nantucket Harbor",
            description="""The Pequod comes into view for the first time, her dark hull 
            and savage decorations foreshadowing the journey ahead.""",
            narrative_tone="foreboding",
            literary_devices=["symbolism", "foreshadowing", "imagery"],
            themes=["destiny", "darkness", "primitive_nature"],
            symbols={
                "savage_decorations": "primitive violence",
                "dark_hull": "hidden dangers",
                "whale_teeth": "predatory nature",
                "tribal_markings": "connection to Queequeg"
            },
            historical_context="Nantucket whaling industry peak",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "queequeg": CharacterTimeline(
                    character_id="queequeg",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "freezing",
                "wind": "strong",
                "visibility": "clear",
                "sea_state": "choppy"
            },
            time_of_day="early_morning",
            calendar_date="December 24, 1850",
            nautical_details={
                "tide": "incoming",
                "ship_state": "anchored",
                "flag_condition": "whipping"
            },
            canonical_text_reference="Now, when I looked about the quarter-deck, for someone having authority...",
        )
        self.plot_events["first_sight_pequod"].initialize_character_positions()

        self.plot_events["christmas_celebration"] = PlotPoint(
            id="christmas_celebration",
            chapter=22,
            title="Christmas Celebration",
            location="Nantucket, Mrs. Hussey's Inn",
            description="""Ishmael and Queequeg celebrate Christmas together, deepening 
            their friendship before embarking on their fateful voyage.""",
            narrative_tone="warm",
            literary_devices=["juxtaposition", "character_development", "cultural_fusion"],
            themes=["friendship", "cultural_exchange", "last_peace"],
            symbols={
                "christmas_feast": "communion",
                "shared_pipe": "brotherhood",
                "warm_hearth": "temporary_haven"
            },
            historical_context="Christian holiday meets pagan customs",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "queequeg": CharacterTimeline(
                    character_id="queequeg",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "warm_indoors",
                "precipitation": "light_snow",
                "indoor_atmosphere": "festive"
            },
            time_of_day="evening",
            calendar_date="December 25, 1850",
            nautical_details={},
            canonical_text_reference="At length we rose and dressed; and Queequeg, taking a prodigiously hearty breakfast...",
        )
        self.plot_events["christmas_celebration"].initialize_character_positions()

        self.plot_events["meeting_ahab"] = PlotPoint(
            id="meeting_ahab",
            chapter=28,
            title="The Pipe",
            location="Pequod, Quarter-deck",
            description="""Captain Ahab finally appears on deck, his ivory leg and the 
            scar that runs down his face marking him as both terrible and magnificent.""",
            narrative_tone="ominous",
            literary_devices=["character_revelation", "symbolism", "foreshadowing"],
            themes=["obsession", "leadership", "destiny"],
            symbols={
                "ivory_leg": "unnatural ambition",
                "lightning_scar": "divine_defiance",
                "pipe": "contemplation_and_torment",
                "quarter_deck": "throne_of_power"
            },
            historical_context="Whaling captain's absolute authority",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "ahab": CharacterTimeline(
                    character_id="ahab",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "starbuck": CharacterTimeline(
                    character_id="starbuck",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "cold",
                "wind": "moderate",
                "sea_state": "rolling",
                "sky": "overcast"
            },
            time_of_day="morning",
            calendar_date="January 1851",
            nautical_details={
                "ship_heading": "southeast",
                "sails": "full",
                "sea_conditions": "following_seas"
            },
            canonical_text_reference="Some days elapsed, and ice and icebergs all astern, the Pequod now went rolling...",
        )
        self.plot_events["meeting_ahab"].initialize_character_positions()

        self.plot_events["first_lowering"] = PlotPoint(
            id="first_lowering",
            chapter=48,
            title="The First Lowering",
            location="Pequod, South Atlantic",
            description="""The crew lowers for whales for the first time, testing their 
            mettle and establishing the hierarchy of the boats.""",
            narrative_tone="tense",
            literary_devices=["action", "character_testing", "natural_symbolism"],
            themes=["initiation", "hierarchy", "man_vs_nature"],
            symbols={
                "whale_boats": "individual_destinies",
                "rough_seas": "life_challenges",
                "harpoons": "human_ambition",
                "whale": "primal_nature"
            },
            historical_context="Whaling industry dangers and procedures",
            character_timelines={
                "ishmael": CharacterTimeline(
                    character_id="ishmael",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "queequeg": CharacterTimeline(
                    character_id="queequeg",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "starbuck": CharacterTimeline(
                    character_id="starbuck",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                "ahab": CharacterTimeline(
                    character_id="ahab",
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "mild",
                "wind": "fresh",
                "sea_state": "moderate",
                "visibility": "good"
            },
            time_of_day="midday",
            calendar_date="February 1851",
            nautical_details={
                "current": "strong",
                "wave_height": "6_feet",
                "wind_direction": "southeast",
                "boat_positions": "scattered"
            },
            canonical_text_reference="The four boats were soon on the water...",
        )
        self.plot_events["first_lowering"].initialize_character_positions()

        self.plot_events["quarter_deck_speech"] = PlotPoint(
            id="quarter_deck_speech",
            chapter=36,
            title="The Quarter-Deck",
            location="Pequod, Quarter-deck",
            description="""Ahab nails the golden doubloon to the mast and reveals his 
            true purpose: hunting theWhite Whale. The crew takes their fatal oath.""",
            narrative_tone="dramatic",
            literary_devices=["dramatic_revelation", "ritual", "oath"],
            themes=["obsession", "manipulation", "fate"],
            symbols={
                "golden_doubloon": "material temptation",
                "hammer_and_nail": "crucifixion",
                "shared_cup": "blood oath",
                "mast": "cross/altar"
            },
            historical_context="Whaling voyage contracts and captain's authority",
            character_timelines={
                'ahab': CharacterTimeline(
                    character_id='ahab',
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                'starbuck': CharacterTimeline(
                    character_id='starbuck',
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                ),
                'ishmael': CharacterTimeline(
                    character_id='ishmael',
                    core_actions=[],
                    optional_actions=[],
                    relationship_states={},
                    knowledge_state={},
                    decision_points=[],
                    action_consequences={}
                )
            },
            weather_conditions={
                "temperature": "moderate",
                "wind": "strong",
                "sea_state": "rough",
                "visibility": "poor"
            },
            time_of_day="afternoon",
            calendar_date="March 1851",
            nautical_details={
                "ship_heading": "southeast",
                "sails": "reefed",
                "sea_depth": "deep"
            },
            canonical_text_reference="And now the time of tide has come; the ship casts off her cables..."
        )
        self.plot_events["quarter_deck_speech"].initialize_character_positions()

        # We need to implement approximately 40 more key plot points
        # Next major events to implement:
        # - The Town-Ho's Story (Ch. 54)
        # - The Spirit-Spout (Ch. 51)
        # - Stubb Kills a Whale (Ch. 61)
        # - The Doubloon (Ch. 99)
        # - The Chase sequences (Ch. 133-135)
        logger.info("Added The Quarter-Deck speech")
        logger.info("Currently implemented 10 out of 50 planned plot points")

    def get_current_choices(self) -> List[StoryChoice]:
        """Get choices based on current plot point and Ishmael's state"""
        if self.current_chapter == 1:
            return [
                StoryChoice(
                    id="to_new_bedford",
                    text="Take the ferry to New Bedford",
                    requirements={},
                    consequences={
                        "location": "spouter_inn_arrival",
                        "chapter": 2,
                        "ishmael_state": {
                            "isolation_level": -0.1,
                            "nautical_skill": 0.1,
                            "physical_condition": -0.1
                        }
                    },
                    emotional_weight={"anticipation": 0.7, "uncertainty": 0.5},
                    available_to=["ishmael"],
                    narrative_weight=0.8
                ),
                StoryChoice(
                    id="reflect_manhattan",
                    text="Wander Manhattan's streets, contemplating the sea",
                    requirements={},
                    consequences={
                        "ishmael_state": {
                            "philosophical_depth": 0.1,
                            "isolation_level": 0.1,
                            "spiritual_awareness": 0.1,
                            "narrative_voice": 0.1
                        }
                    },
                    emotional_weight={"melancholy": 0.6, "contemplation": 0.8},
                    available_to=["ishmael"],
                    narrative_weight=0.4
                )
            ]
        elif self.current_chapter == 2:
            return [
                StoryChoice(
                    id="enter_spouter",
                    text="Enter the Spouter-Inn",
                    requirements={},
                    consequences={
                        "location": "spouter_inn_inside",
                        "chapter": 3,
                        "ishmael_state": {"isolation_level": -0.2}
                    },
                    emotional_weight={"curiosity": 0.6, "apprehension": 0.4},
                    available_to=["ishmael"],
                    narrative_weight=0.9
                ),
                StoryChoice(
                    id="explore_bedford",
                    text="Explore New Bedford's waterfront",
                    requirements={},
                    consequences={
                        "ishmael_state": {"knowledge_of_whaling": 0.1}
                    },
                    emotional_weight={"curiosity": 0.7, "wonder": 0.5},
                    available_to=["ishmael"],
                    narrative_weight=0.3
                )
            ]
        return []

    def make_choice(self, choice_id: str) -> Dict[str, Any]:
        """Process choice and update story state"""
        try:
            logger.info("Processing choice: %s", choice_id)
            choices = self.get_current_choices()
            selected_choice = next((c for c in choices if c.id == choice_id), None)

            if not selected_choice:
                return {"status": "error", "message": "Invalid choice"}

            # Update Ishmael's state based on choice consequences
            if "ishmael_state" in selected_choice.consequences:
                for attr, change in selected_choice.consequences["ishmael_state"].items():
                    current_value = getattr(self.ishmael_state, attr)
                    new_value = max(0, min(1, current_value + change))
                    setattr(self.ishmael_state, attr, new_value)

            # Update chapter if specified
            if "chapter" in selected_choice.consequences:
                self.current_chapter = selected_choice.consequences["chapter"]

            # Get the next plot point
            next_event = self.plot_events.get(
                selected_choice.consequences.get("location", "manhattan_departure")
            )

            # Record choice and state
            self.history.append({
                'choice_id': choice_id,
                'timestamp': datetime.now().isoformat(),
                'ishmael_state': self.ishmael_state.__dict__.copy(),
                'plot_point': next_event.id if next_event else None,
                'character_positions': next_event.character_positions if next_event else {}
            })

            return {
                "status": "success",
                "plot_point": next_event,
                "ishmael_state": self.ishmael_state,
                "choices": self.get_current_choices()
            }
        except Exception as e:
            logger.error("Error processing choice: %s", str(e))
            return {'status': 'error', 'message': str(e)}

    def get_narrative_context(self) -> Dict[str, Any]:
        """Get rich context about the current story state"""
        try:
            logger.info("Getting narrative context for chapter %d", self.current_chapter)
            current_plot = self.plot_events[
                "spouter_inn_arrival" if self.current_chapter > 1 else "manhattan_departure"
            ]

            return {
                "chapter": self.current_chapter,
                "plot_point": current_plot,
                "ishmael_state": self.ishmael_state,
                "available_choices": self.get_current_choices(),
                "narrative_themes": current_plot.themes,
                "literary_context": {
                    "devices": current_plot.literary_devices,
                    "symbols": current_plot.symbols,
                    "historical_context": current_plot.historical_context
                },
                "character_positions": current_plot.character_positions
            }
        except Exception as e:
            logger.error("Error getting narrative context: %s", str(e))
            return {
                'chapter': 1,
                'plot_point': {
                    'description': 'The story begins...',
                    'location': 'Unknown',
                    'event_description': 'Error loading story state.'
                },
                'character_positions': {},
                'available_choices': []
            }

    def evaluate_story_state(self) -> Dict[str, Any]:
        """Analyze current story state and divergence level"""
        if not self.current_branch:
            return {
                'divergence_level': 0.0,
                'canonical_possible': True,
                'thematic_alignment': 1.0
            }

        # Calculate cumulative divergence from all branches
        total_divergence = sum(
            1.0 - branch.thematic_consistency
            for branch in self.branch_history
        ) / max(len(self.branch_history), 1)

        # Check if we're past the point of no return
        canonical_possible = total_divergence < self.divergence_threshold

        # If we're at ~80% through the story (around chapter 100 of 125)
        story_progress = self.current_chapter / 125
        if story_progress > 0.8 and not canonical_possible:
            self.trigger_ending_decision()

        return {
            'divergence_level': total_divergence,
            'canonical_possible': canonical_possible,
            'thematic_alignment': 1.0 - total_divergence,
            'requires_alternate_ending': not canonical_possible and story_progress > 0.8
        }

    def trigger_ending_decision(self) -> Dict[str, Any]:
        """Present the player with a crucial decision about the story's direction"""
        # Get current themes and character states
        active_themes = self._analyze_active_themes()
        character_states = self._get_character_states()

        # Generate possible alternate endings based on choices so far
        alternate_paths = self._generate_alternate_paths(active_themes, character_states)

        return {
            'message': (
                "Your choices have led to a fundamentally different story. "
                "The time has come to decide how your version of Moby Dick will end."
            ),
            'current_themes': active_themes,
            'character_states': character_states,
            'alternate_paths': alternate_paths,
            'original_ending': self._get_canonical_ending_summary()
        }

    def _analyze_active_themes(self) -> Dict[str, float]:
        """Analyze which themes are most prominent in current branch"""
        themes = {}
        for branch in self.branch_history:
            for theme, strength in branch.thematic_elements.items():
                themes[theme] = max(themes.get(theme, 0), strength)
        return themes

    def _get_character_states(self) -> Dict[str, Dict[str, Any]]:
        """Get current state and development arc of each character"""
        states = {}
        for char_id, timeline in self.current_plot.character_timelines.items():
            states[char_id] = {
                'development_arc': self._analyze_character_arc(timeline),
                'relationships': timeline.relationship_states.copy(),
                'key_actions': [
                    action.description for action in timeline.core_actions[-3:]
                ]  # Last 3 significant actions
            }
        return states

    def _generate_alternate_paths(
        self,
        themes: Dict[str, float],
        char_states: Dict[str, Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Generate possible alternate endings based on current state"""
        paths = []

        # Example alternate ending focused on redemption
        if themes.get('redemption', 0) > 0.6:
            paths.append({
                'type': 'redemption',
                'description': 'Ahab realizes the cost of his obsession and chooses a different path',
                'theme_alignment': 0.8,
                'character_resolutions': {
                    'ahab': 'finds peace',
                    'ishmael': 'gains wisdom',
                    'starbuck': 'proves his moral strength'
                }
            })

        # Example alternate ending focused on nature's supremacy
        if themes.get('nature', 0) > 0.6:
            paths.append({
                'type': 'nature_wins',
                'description': 'The white whale proves ultimately unknowable and untameable',
                'theme_alignment': 0.9,
                'character_resolutions': {
                    'ahab': 'faces the limits of human will',
                    'ishmael': 'accepts nature\'s mysteries',
                    'pequod': 'returns changed but intact'
                }
            })

        return paths

    def _analyze_character_arc(self, timeline: CharacterTimeline) -> str:
        """Analyze a character's development through the story"""
        # Placeholder:  This needs a more sophisticated analysis
        return "Character arc needs further implementation"

    def _get_canonical_ending_summary(self) -> str:
        """Summarize the canonical ending of Moby Dick"""
        return "Canonical ending summary needs implementation"

    def create_story_branch(self, 
                     canonical_action: CharacterAction,
                     player_choice: Dict[str, Any]) -> StoryBranch:
        """Create a new branch when player deviates from canon"""
        branch_id = f"branch_{len(self.branch_history) + 1}"

        # Create alternate action based on player choice
        alternate_action = CharacterAction(
            character_id=canonical_action.character_id,
            action_type=player_choice['type'],
            description=player_choice['description'],
            direct_impact=player_choice.get('impact', ''),
            causal_chain=[],  # To be generated
            influenced_characters={},
            timestamp=datetime.now(),
            location=canonical_action.location,
            witnesses=canonical_action.witnesses,
            story_significance=canonical_action.story_significance,
            player_choices={},
            knowledge_requirements=canonical_action.knowledge_requirements,
            agency_points=[],
            canonical_text_reference=''
        )

        # Calculate thematic consistency
        thematic_alignment = self._calculate_thematic_alignment(
            canonical_action, alternate_action
        )

        # Create branch
        branch = StoryBranch(
            branch_id=branch_id,
            divergence_point=canonical_action.canonical_text_reference,
            canonical_action=canonical_action,
            alternate_action=alternate_action,
            consequences=[],  # To be generated
            thematic_consistency=thematic_alignment,
            character_impacts=self._calculate_character_impacts(
                canonical_action, alternate_action
            ),
            is_point_of_no_return=False  # Will be evaluated later
        )

        # Evaluate narrative tension
        tensions = branch.evaluate_narrative_tension()

        # Check if this creates a point of no return
        if (branch.narrative_tension > self.divergence_threshold and 
            self.current_chapter > 100):  # Late in the story
            branch.is_point_of_no_return = True
            branch.alternate_ending_required = True

        self.branch_history.append(branch)
        self.current_branch = branch

        return branch

    def _calculate_thematic_alignment(self, 
                              canonical: CharacterAction, 
                              alternate: CharacterAction) -> float:
        """Calculate how well alternate action aligns with original themes"""
        # Get themes from current plot point
        current_themes = self.current_plot.themes if self.current_plot else []

        # Basic thematic analysis (to be enhanced with AI)
        alignment_score = 0.8  # Start with high alignment

        # Reduce alignment for major deviations
        if canonical.action_type != alternate.action_type:
            alignment_score -= 0.2

        # Check if alternate action maintains key themes
        for theme in current_themes:
            if theme.lower() not in alternate.description.lower():
                alignment_score -= 0.1

        return max(0.0, min(1.0, alignment_score))

    def _calculate_character_impacts(self,
                             canonical: CharacterAction,
                             alternate: CharacterAction) -> Dict[str, Dict[str, Any]]:
        """Calculate how alternate action impacts each character"""
        impacts = {}

        # Example impact calculation for main characters
        for char_id in ['ishmael', 'queequeg', 'ahab', 'starbuck']:
            if char_id in canonical.influenced_characters:
                canonical_impact = canonical.influenced_characters[char_id]
                alternate_impact = alternate.influenced_characters.get(char_id, '')

                severity = 0.5  # Default medium impact
                if canonical_impact != alternate_impact:
                    severity = 0.8  # High impact for different outcomes

                impacts[char_id] = {
                    'canonical_outcome': canonical_impact,
                    'alternate_outcome': alternate_impact,
                    'severity': severity
                }

        return impacts

    def get_character_view(self, character_id: str) -> Dict[str, Any]:
        """Get story state from a specific character's perspective"""
        if character_id not in self.character_perceptions:
            logger.warning(f"No perception found for character {character_id}")
            return {}  # Return empty dict instead of None

        perception = self.character_perceptions[character_id]
        filtered_choices = []

        for choice in self.available_choices:
            if character_id in choice.available_to:
                # Check if character meets requirements
                meets_requirements = True
                for req, value in choice.requirements.items():
                    if req.startswith('knowledge_') and not perception.knowledge_state.get(req[9:], False):
                        meets_requirements = False
                        break
                if meets_requirements:
                    filtered_choices.append(choice)

        return {
            "what_happened": perception.interpretation,
            "emotions": perception.emotional_response,
            "observations": perception.sensory_details,
            "thoughts": perception.inner_monologue,
            "available_choices": filtered_choices,
            "atmosphere": self.atmosphere
        }

    def get_plot_point_by_id(self, plot_id: str) -> Optional[PlotPoint]:
        """Get a plot point by its ID"""
        if not plot_id or plot_id not in self.plot_events:
            logger.warning(f"Plot point {plot_id} not found")
            return None
        return self.plot_events[plot_id]

    def get_character_timelines(self, plot_point: Optional[PlotPoint]) -> Dict[str, CharacterTimeline]:
        """Safely get character timelines from a plot point"""
        if not plot_point:
            logger.warning("No plot point provided for character timelines")
            return {}
        return plot_point.character_timelines

# Initialize the global instance with error handling
try:
    story_engine = StoryEngine()
    logger.info("Global story_engine instance created successfully")
except Exception as e:
    logger.error("Failed to create global story_engine instance: %s", str(e))
    raise