"""Test suite for narrative ontology system with Frye's archetypal patterns"""
import pytest
from .narrative_ontology import (
    NarrativeOntologyBuilder, 
    FryeMythos, 
    FryeanPattern,
    TimelineNode,
    CharacterAction
)

def test_frye_pattern_recognition():
    """Test recognition of Frye's archetypal patterns"""
    ontology = NarrativeOntologyBuilder()

    # Create test timeline nodes with tragic pattern
    tragic_nodes = [
        TimelineNode(
            id="1",
            title="The Fall",
            description="The proud king stood atop his castle, unaware of his impending fall.",
            thematic_elements={"pride": 0.9, "fate": 0.8, "hubris": 0.7},
            character_actions={
                "king": [CharacterAction(
                    character_id="king",
                    action_text="The tragic hero contemplated his destiny",
                    impact_level=0.8,
                    is_canonical=True,
                    thematic_elements={"pride": 0.9, "fate": 0.8},
                    consequences=["2"]
                )]
            },
            characters_present=["king", "advisor"],
            location="castle",
            next_nodes=["2"],
            requirements={"previous_chapter": 0.8},
            proximity_data={"castle": 1.0}
        ),
        TimelineNode(
            id="2",
            title="The Storm",
            description="Storm clouds gathered as the prophecy began to unfold.",
            thematic_elements={"fate": 0.9, "justice": 0.8},
            character_actions={
                "chorus": [CharacterAction(
                    character_id="chorus",
                    action_text="The chorus warned of divine retribution",
                    impact_level=0.7,
                    is_canonical=True,
                    thematic_elements={"fate": 0.9, "justice": 0.8},
                    consequences=[]
                )]
            },
            characters_present=["chorus", "king"],
            location="palace",
            next_nodes=[],
            requirements={"previous_scene": 0.7},
            proximity_data={"palace": 1.0}
        )
    ]

    # Analyze patterns
    patterns = ontology._analyze_frye_patterns(tragic_nodes)

    # Verify tragedy pattern was detected
    assert any(p.mythos == FryeMythos.TRAGEDY for p in patterns)
    tragedy = next(p for p in patterns if p.mythos == FryeMythos.TRAGEDY)
    assert tragedy.resonance > 0.5

    # Check thematic elements
    assert "fate" in tragedy.thematic_elements
    assert "pride" in tragedy.thematic_elements

    # Check character types
    assert "tragic hero" in tragedy.character_types
    assert "chorus" in tragedy.character_types

def test_pattern_resonance_calculation():
    """Test calculation of pattern resonance strength"""
    ontology = NarrativeOntologyBuilder()

    # Create a test pattern
    test_pattern = FryeanPattern(
        mythos=FryeMythos.TRAGEDY,
        phase=1,
        character_types={"tragic hero", "chorus"},
        plot_movements=["hubris", "prophecy", "fall"],
        symbols={"storm", "crown", "throne"},
        thematic_elements={"pride", "fate", "justice"},
        typical_conflicts=[("individual", "fate")]
    )

    # Create test node with strong tragic elements
    strong_node = TimelineNode(
        id="1",
        title="The Crown Falls",
        description="The storm raged as the crown fell from the king's head.",
        thematic_elements={"pride": 0.9, "fate": 0.8},
        character_actions={
            "king": [CharacterAction(
                character_id="king",
                action_text="The tragic hero defied the prophecy",
                impact_level=0.8,
                is_canonical=True,
                thematic_elements={"pride": 0.9, "fate": 0.8},
                consequences=["2"]
            )],
            "chorus": [CharacterAction(
                character_id="chorus",
                action_text="The chorus lamented the hero's pride",
                impact_level=0.7,
                is_canonical=True,
                thematic_elements={"pride": 0.8},
                consequences=[]
            )]
        },
        characters_present=["king", "chorus"],
        location="throne_room",
        next_nodes=["2"],
        requirements={"previous_scene": 0.8},
        proximity_data={"throne_room": 1.0}
    )

    resonance = ontology._calculate_pattern_resonance(test_pattern, [strong_node])
    assert resonance > 0.6  # Strong resonance threshold

def test_mythos_classification():
    """Test classification of narrative into Frye's mythoi"""
    ontology = NarrativeOntologyBuilder()

    # Create comic nodes
    comic_nodes = [
        TimelineNode(
            id="1",
            title="Spring Love",
            description="Spring flowers bloomed as young lovers met in the garden.",
            thematic_elements={"love": 0.9, "youth": 0.8, "renewal": 0.7},
            character_actions={
                "hero": [CharacterAction(
                    character_id="hero",
                    action_text="The young lover planned to overcome obstacles",
                    impact_level=0.8,
                    is_canonical=True,
                    thematic_elements={"love": 0.9, "youth": 0.8},
                    consequences=["garden_meeting"]
                )],
                "helper": [CharacterAction(
                    character_id="helper",
                    action_text="The wise servant devised a plan",
                    impact_level=0.6,
                    is_canonical=True,
                    thematic_elements={"wisdom": 0.7},
                    consequences=[]
                )]
            },
            characters_present=["hero", "helper"],
            location="garden",
            next_nodes=["garden_meeting"],
            requirements={"daylight": 0.8},
            proximity_data={"garden": 1.0}
        )
    ]

    patterns = ontology._analyze_frye_patterns(comic_nodes)
    assert any(p.mythos == FryeMythos.COMEDY for p in patterns)
    comedy = next(p for p in patterns if p.mythos == FryeMythos.COMEDY)
    assert comedy.resonance > 0.5

def test_frye_mythos_classification():
    """Test basic classification of narratives into Frye's mythoi"""
    ontology = NarrativeOntologyBuilder()

    # Test tragic narrative
    tragic_nodes = [
        TimelineNode(
            id="1",
            title="The Fall",
            description="The proud king stood atop his castle, unaware of his impending fall.",
            thematic_elements={"pride": 0.9, "fate": 0.8, "hubris": 0.7},
            character_actions={
                "king": [CharacterAction(
                    character_id="king",
                    action_text="The tragic hero contemplated his destiny",
                    impact_level=0.8,
                    is_canonical=True,
                    thematic_elements={"pride": 0.9, "fate": 0.8},
                    consequences=["2"]
                )]
            },
            characters_present=["king", "advisor"],
            location="castle",
            next_nodes=["2"],
            requirements={"previous_chapter": 0.8},
            proximity_data={"castle": 1.0}
        ),
        TimelineNode(
            id="2",
            title="The Storm",
            description="Storm clouds gathered as the prophecy began to unfold.",
            thematic_elements={"fate": 0.9, "justice": 0.8},
            character_actions={
                "chorus": [CharacterAction(
                    character_id="chorus",
                    action_text="The chorus warned of divine retribution",
                    impact_level=0.7,
                    is_canonical=True,
                    thematic_elements={"fate": 0.9, "justice": 0.8},
                    consequences=[]
                )]
            },
            characters_present=["chorus", "king"],
            location="palace",
            next_nodes=[],
            requirements={"previous_scene": 0.7},
            proximity_data={"palace": 1.0}
        )
    ]

    patterns = ontology._analyze_frye_patterns(tragic_nodes)
    assert any(p.mythos == FryeMythos.TRAGEDY for p in patterns), "Failed to identify tragic mythos"
    tragedy = next(p for p in patterns if p.mythos == FryeMythos.TRAGEDY)
    assert tragedy.resonance > 0.5, "Tragic resonance too weak"

def test_pattern_phase_tracking():
    """Test tracking of phases within a mythos pattern"""
    ontology = NarrativeOntologyBuilder()

    # Test comic pattern through phases
    comic_nodes = [
        TimelineNode(
            id="1",
            title="Spring Meeting",
            description="Spring flowers bloomed as young lovers met in the garden.",
            thematic_elements={"love": 0.9, "youth": 0.8, "renewal": 0.7},
            character_actions={
                "hero": [CharacterAction(
                    character_id="hero",
                    action_text="The young lover planned to overcome obstacles",
                    impact_level=0.8,
                    is_canonical=True,
                    thematic_elements={"love": 0.9, "youth": 0.8},
                    consequences=["2"]
                )],
                "helper": [CharacterAction(
                    character_id="helper",
                    action_text="The wise servant devised a plan",
                    impact_level=0.6,
                    is_canonical=True,
                    thematic_elements={"wisdom": 0.7},
                    consequences=["2"]
                )]
            },
            characters_present=["hero", "helper"],
            location="garden",
            next_nodes=["2"],
            requirements={"daylight": 0.8},
            proximity_data={"garden": 1.0}
        ),
        TimelineNode(
            id="2",
            title="Resolution",
            description="The festival brought all together in joyous celebration.",
            thematic_elements={"harmony": 0.9, "reconciliation": 0.8},
            character_actions={
                "hero": [CharacterAction(
                    character_id="hero",
                    action_text="The lovers united despite all obstacles",
                    impact_level=0.9,
                    is_canonical=True,
                    thematic_elements={"love": 1.0, "harmony": 0.9},
                    consequences=[]
                )]
            },
            characters_present=["hero", "helper", "society"],
            location="festival_grounds",
            next_nodes=[],
            requirements={"previous_scene": 0.8},
            proximity_data={"festival_grounds": 1.0}
        )
    ]

    patterns = ontology._analyze_frye_patterns(comic_nodes)
    comedy = next(p for p in patterns if p.mythos == FryeMythos.COMEDY)
    assert comedy.phase in [1, 2], "Comic phase not properly identified"
    assert "festival" in comedy.symbols, "Failed to identify key comic symbol"
    assert ("youth", "age") in comedy.typical_conflicts, "Failed to identify typical comic conflict"

def test_pattern_recognition_implementation():
    """Test the full pattern recognition implementation"""
    ontology = NarrativeOntologyBuilder()

    # Test ironic/satiric pattern
    ironic_nodes = [
        TimelineNode(
            id="1",
            title="The Office",
            description="In the maze-like corporate office, the employee preferred not to.",
            thematic_elements={"alienation": 0.9, "absurdity": 0.8},
            character_actions={
                "bartleby": [CharacterAction(
                    character_id="bartleby",
                    action_text="The scrivener quietly resisted society's demands",
                    impact_level=0.9,
                    is_canonical=True,
                    thematic_elements={"resistance": 0.9, "alienation": 0.8},
                    consequences=[]
                )],
            },
            characters_present=["bartleby", "lawyer"],
            location="office",
            next_nodes=[],
            requirements={"previous_scene": 0.7},
            proximity_data={"office": 1.0}
        )
    ]

    # Analyze patterns
    patterns = ontology._analyze_frye_patterns(ironic_nodes)

    # Verify ironic pattern detection
    assert any(p.mythos == FryeMythos.IRONY for p in patterns), "Failed to identify ironic mythos"
    irony = next(p for p in patterns if p.mythos == FryeMythos.IRONY)

    # Check pattern elements
    assert "maze" in irony.symbols, "Failed to identify key ironic symbol"
    assert "alienation" in irony.thematic_elements, "Failed to identify key ironic theme"
    assert any("society" in conflict for conflict in irony.typical_conflicts), "Failed to identify societal conflict"
    assert irony.resonance > 0.4, "Ironic resonance too weak"

if __name__ == "__main__":
    pytest.main([__file__])