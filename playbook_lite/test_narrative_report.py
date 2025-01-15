"""Test the narrative ontology report generation"""
import pytest
from datetime import datetime
from .story_types import TimelineNode, CharacterAction
from .narrative_report import NarrativeOntologyReport

def create_test_timeline(title: str) -> list[TimelineNode]:
    """Create test timeline nodes for a novel"""
    if title == "Moby Dick":
        return [
            TimelineNode(
                id="1",
                title="Call me Ishmael",
                description="A young man seeks escape from depression through seafaring.",
                thematic_elements={"isolation": 0.9, "quest": 0.8, "identity": 0.7},
                character_actions={
                    "ishmael": [CharacterAction(
                        character_id="ishmael",
                        action_text="The narrator introduces himself and his motivations",
                        impact_level=0.8,
                        thematic_elements={"isolation": 0.9, "identity": 0.7},
                        consequences=["2"]
                    )]
                },
                characters_present=["ishmael"],
                location="manhattan",
                next_nodes=["2"],
                requirements={"previous_chapter": 0.0},
                proximity_data={"ishmael": {"manhattan": 1.0}}
            ),
            TimelineNode(
                id="2",
                title="The Sermon",
                description="Father Mapple delivers his powerful sermon on Jonah.",
                thematic_elements={"faith": 0.9, "duty": 0.8, "defiance": 0.7},
                character_actions={
                    "father_mapple": [CharacterAction(
                        character_id="father_mapple",
                        action_text="The preacher warns of divine judgment",
                        impact_level=0.9,
                        thematic_elements={"faith": 0.9, "duty": 0.8},
                        consequences=[]
                    )]
                },
                characters_present=["father_mapple", "ishmael", "queequeg"],
                location="whaleman's_chapel",
                next_nodes=[],
                requirements={"previous_scene": 0.8},
                proximity_data={"father_mapple": {"chapel": 1.0}}
            )
        ]
    elif title == "Pride and Prejudice":
        return [
            TimelineNode(
                id="1",
                title="A Truth Universally Acknowledged",
                description="The arrival of a wealthy bachelor stirs a neighborhood.",
                thematic_elements={"marriage": 0.9, "class": 0.8, "prejudice": 0.7},
                character_actions={
                    "mrs_bennet": [CharacterAction(
                        character_id="mrs_bennet",
                        action_text="The mother plots advantageous marriages",
                        impact_level=0.7,
                        thematic_elements={"marriage": 0.9, "class": 0.8},
                        consequences=["2"]
                    )]
                },
                characters_present=["mrs_bennet", "mr_bennet"],
                location="longbourn",
                next_nodes=["2"],
                requirements={"previous_chapter": 0.0},
                proximity_data={"mrs_bennet": {"longbourn": 1.0}}
            ),
            TimelineNode(
                id="2",
                title="First Impressions",
                description="Elizabeth forms her initial opinion of Mr. Darcy.",
                thematic_elements={"pride": 0.9, "prejudice": 0.8, "judgment": 0.7},
                character_actions={
                    "elizabeth": [CharacterAction(
                        character_id="elizabeth",
                        action_text="The heroine judges harshly",
                        impact_level=0.8,
                        thematic_elements={"pride": 0.8, "prejudice": 0.9},
                        consequences=[]
                    )]
                },
                characters_present=["elizabeth", "darcy", "bingley"],
                location="meryton_assembly",
                next_nodes=[],
                requirements={"previous_scene": 0.7},
                proximity_data={"elizabeth": {"assembly_room": 1.0}}
            )
        ]
    return []

def test_narrative_report_generation():
    """Test generating narrative ontology reports"""
    report_gen = NarrativeOntologyReport()

    # Analyze test novels
    novels = ["Moby Dick", "Pride and Prejudice"]
    for title in novels:
        timeline = create_test_timeline(title)
        analysis = report_gen.analyze_novel(
            title=title,
            author="Test Author",
            timeline_nodes=timeline
        )
        report_gen.analyses[title] = analysis

    # Generate comparative report
    report = report_gen.generate_comparative_report(novels)

    # Verify report contents
    assert "NARRATIVE ONTOLOGY REPORT" in report
    assert "PRIMARY NARRATIVE PATTERNS" in report
    assert "PATTERN VISUALIZATION" in report

    # Verify each novel is analyzed
    for title in novels:
        assert title in report

    # Check for pattern visualization
    assert "█" in report  # Primary pattern visualization
    assert "░" in report  # Frye pattern visualization

def test_individual_analysis():
    """Test analysis of a single novel"""
    report_gen = NarrativeOntologyReport()

    # Analyze Moby Dick
    timeline = create_test_timeline("Moby Dick")
    analysis = report_gen.analyze_novel(
        title="Moby Dick",
        author="Herman Melville",
        timeline_nodes=timeline
    )

    # Verify analysis results
    assert analysis.title == "Moby Dick"
    assert analysis.author == "Herman Melville"
    assert analysis.narrative_tension > 0
    assert len(analysis.key_themes) > 0
    assert len(analysis.character_archetypes) > 0
    assert len(analysis.primary_patterns) > 0
    assert len(analysis.unique_elements) >= 0

    # Verify Frye's patterns are present but secondary
    assert isinstance(analysis.frye_resonance, dict)
    assert len(analysis.frye_resonance) > 0

if __name__ == "__main__":
    pytest.main([__file__])