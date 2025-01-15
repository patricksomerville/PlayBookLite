"""Generate comparative narrative ontology reports for novels"""
import logging
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from .story_types import TimelineNode, CharacterAction
from .narrative_ontology import NarrativeOntologyBuilder, FryeMythos, FryeanPattern

logger = logging.getLogger(__name__)

@dataclass
class NovelAnalysis:
    """Analysis results for a single novel"""
    title: str
    author: str
    primary_patterns: List[str]  # Our own identified patterns
    frye_resonance: Dict[FryeMythos, float]  # Frye's patterns as secondary insight
    key_themes: List[str]
    character_archetypes: Dict[str, str]
    narrative_tension: float
    symbolic_density: float
    unique_elements: List[str]  # Elements that don't fit traditional patterns

@dataclass
class ComparativeInsight:
    """Comparative analysis between novels"""
    shared_patterns: List[str]
    thematic_overlaps: Dict[str, List[str]]
    archetypal_similarities: Dict[str, List[str]]
    unique_innovations: Dict[str, str]  # Novel-specific narrative innovations

class NarrativeOntologyReport:
    """Generate comparative reports analyzing narrative patterns across novels"""

    def __init__(self):
        self.ontology = NarrativeOntologyBuilder()
        self.analyses: Dict[str, NovelAnalysis] = {}

    def analyze_novel(self, title: str, author: str, timeline_nodes: List[TimelineNode]) -> NovelAnalysis:
        """Analyze a single novel's narrative patterns"""
        logger.info(f"Analyzing patterns for {title} by {author}")

        # Our primary analysis
        primary_patterns = self._analyze_novel_patterns(timeline_nodes)

        # Frye's patterns as secondary insight
        frye_patterns = self.ontology._analyze_frye_patterns(timeline_nodes)
        frye_resonance = {
            mythos: max((p.resonance for p in frye_patterns if p.mythos == mythos), default=0.0)
            for mythos in FryeMythos
        }

        # Extract key themes
        themes = set()
        for node in timeline_nodes:
            themes.update(node.thematic_elements.keys())

        # Identify character archetypes
        archetypes = {}
        for node in timeline_nodes:
            for char in node.characters_present:
                actions = [
                    action for actions in node.character_actions.values()
                    for action in actions if action.character_id == char
                ]
                archetypes[char] = self._determine_archetype(actions)

        # Calculate narrative tension
        tension = sum(
            action.impact_level
            for node in timeline_nodes
            for actions in node.character_actions.values()
            for action in actions
        ) / len(timeline_nodes)

        # Identify unique elements
        unique_elements = self._identify_unique_elements(timeline_nodes)

        # Calculate symbolic density
        symbolic_density = len(set(
            theme for node in timeline_nodes
            for theme in node.thematic_elements.keys()
        )) / len(timeline_nodes)

        return NovelAnalysis(
            title=title,
            author=author,
            primary_patterns=primary_patterns,
            frye_resonance=frye_resonance,
            key_themes=sorted(themes),
            character_archetypes=archetypes,
            narrative_tension=tension,
            symbolic_density=symbolic_density,
            unique_elements=unique_elements
        )

    def _analyze_novel_patterns(self, nodes: List[TimelineNode]) -> List[str]:
        """Identify narrative patterns unique to this work"""
        patterns = []

        # Analyze theme progression
        theme_progression = self._analyze_theme_progression(nodes)
        if theme_progression:
            patterns.append(f"Theme progression: {theme_progression}")

        # Analyze character dynamics
        character_dynamics = self._analyze_character_dynamics(nodes)
        if character_dynamics:
            patterns.append(f"Character dynamics: {character_dynamics}")

        # Look for structural innovations
        structural_patterns = self._analyze_structural_patterns(nodes)
        patterns.extend(structural_patterns)

        return patterns

    def _determine_archetype(self, actions: List[CharacterAction]) -> str:
        """Determine character archetype from their actions"""
        if not actions:
            return "Unknown"

        # Analyze action impacts and themes
        impacts = [action.impact_level for action in actions]
        themes = [
            theme
            for action in actions
            for theme, value in action.thematic_elements.items()
            if value > 0.6
        ]

        # Look for unique character types first
        if "resistance" in themes and "alienation" in themes:
            return "Social Critic"
        elif "wisdom" in themes and "doubt" in themes:
            return "Questioning Guide"
        elif "duty" in themes and "conscience" in themes:
            return "Moral Struggler"

        # Fall back to more traditional archetypes
        if sum(impacts) / len(impacts) > 0.7:
            return "Principal Actor"
        elif "wisdom" in themes:
            return "Guide"
        else:
            return "Supporting Character"

    def _identify_unique_elements(self, nodes: List[TimelineNode]) -> List[str]:
        """Identify narrative elements that deviate from traditional patterns"""
        unique_elements = []

        # Look for unusual theme combinations
        theme_pairs = set()
        for node in nodes:
            themes = list(node.thematic_elements.items())
            for i, (theme1, value1) in enumerate(themes):
                for theme2, value2 in themes[i+1:]:
                    if value1 > 0.7 and value2 > 0.7:
                        theme_pairs.add((theme1, theme2))

        unusual_pairs = [
            f"Unexpected theme combination: {t1} + {t2}"
            for t1, t2 in theme_pairs
            if self._is_unusual_combination(t1, t2)
        ]
        unique_elements.extend(unusual_pairs)

        return unique_elements

    def _is_unusual_combination(self, theme1: str, theme2: str) -> bool:
        """Check if a theme combination is unusual"""
        common_pairs = {
            ("love", "sacrifice"),
            ("duty", "honor"),
            ("fate", "free_will"),
            ("pride", "prejudice"),  # Added as it's a common pairing
            ("isolation", "identity")  # Added for Moby Dick's themes
        }
        return (theme1, theme2) not in common_pairs and (theme2, theme1) not in common_pairs

    def _analyze_theme_progression(self, nodes: List[TimelineNode]) -> Optional[str]:
        """Analyze how themes progress through the narrative"""
        if not nodes:
            return None

        theme_strengths = {}
        for node in nodes:
            for theme, strength in node.thematic_elements.items():
                if theme not in theme_strengths:
                    theme_strengths[theme] = []
                theme_strengths[theme].append(strength)

        # Look for interesting progressions
        progressions = []
        for theme, strengths in theme_strengths.items():
            if len(strengths) < 2:
                continue

            if strengths[-1] > strengths[0] + 0.3:
                progressions.append(f"Rising {theme}")
            elif strengths[0] > strengths[-1] + 0.3:
                progressions.append(f"Declining {theme}")
            elif max(strengths) > min(strengths) + 0.4:
                progressions.append(f"Fluctuating {theme}")

        if progressions:
            return ", ".join(progressions)
        return None

    def generate_comparative_report(self, novels: List[str]) -> str:
        """Generate a one-page comparative report for the given novels"""
        report = ["NARRATIVE ONTOLOGY REPORT", "=" * 80, ""]
        report.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")

        # Individual novel analyses
        report.append("PRIMARY NARRATIVE PATTERNS")
        report.append("-" * 40)
        for title in novels:
            analysis = self.analyses.get(title)
            if not analysis:
                continue

            # Report primary patterns first
            report.extend([
                f"\n{analysis.title} by {analysis.author}",
                "Primary Patterns:",
                *[f"- {pattern}" for pattern in analysis.primary_patterns[:3]],
                f"Key Themes: {', '.join(analysis.key_themes[:5])}",
                "Unique Elements:",
                *[f"- {element}" for element in analysis.unique_elements[:2]],
                f"Narrative Tension: {analysis.narrative_tension:.2f}\n"
            ])

            # Add Frye's patterns as secondary insight
            report.extend([
                "Secondary Analysis (Frye's Patterns):",
                *[f"- {mythos.value}: {resonance:.2f}" for mythos, resonance in analysis.frye_resonance.items() if resonance > 0.1],
                "\n"
            ])

        # Pattern visualization
        report.extend([
            "\nPATTERN VISUALIZATION",
            "-" * 40,
            self._generate_pattern_visualization(novels)
        ])

        return "\n".join(report)

    def _generate_pattern_visualization(self, novels: List[str]) -> str:
        """Generate ASCII visualization of pattern distribution"""
        MAX_WIDTH = 40
        vis = []

        for title in novels:
            analysis = self.analyses.get(title)
            if not analysis:
                continue

            vis.append(f"\n{title}:")

            # Show primary patterns with solid blocks
            for pattern in analysis.primary_patterns[:3]:
                bar_width = int(analysis.narrative_tension * MAX_WIDTH)
                vis.append(f"{pattern[:15]:15} {'█' * bar_width}{' ' * (MAX_WIDTH - bar_width)}")

            # Show Frye patterns with light blocks
            vis.append("\nFrye Resonance:")
            for mythos, resonance in sorted(analysis.frye_resonance.items(), key=lambda x: x[1], reverse=True):
                bar_width = int(resonance * MAX_WIDTH)
                if resonance > 0.1:  # Only show significant resonances
                    vis.append(f"{mythos.value:10} {'░' * bar_width}{' ' * (MAX_WIDTH - bar_width)} {resonance:.2f}")

        return "\n".join(vis)

    def _analyze_character_dynamics(self, nodes: List[TimelineNode]) -> Optional[str]:
        """Analyze character interactions and development"""
        if not nodes:
            return None

        # Track character presence
        presence = {}
        for node in nodes:
            for char in node.characters_present:
                if char not in presence:
                    presence[char] = 0
                presence[char] += 1

        # Identify key character dynamics
        dynamics = []
        for char, count in presence.items():
            if count == len(nodes):
                dynamics.append(f"Constant presence: {char}")
            elif count == 1:
                dynamics.append(f"Singular appearance: {char}")

        if dynamics:
            return ", ".join(dynamics)
        return None
    def _analyze_structural_patterns(self, nodes: List[TimelineNode]) -> List[str]:
        """Analyze structural patterns in the narrative"""
        patterns = []

        # Look for circular structure
        if len(nodes) > 1:
            first_themes = set(nodes[0].thematic_elements.keys())
            last_themes = set(nodes[-1].thematic_elements.keys())
            if len(first_themes.intersection(last_themes)) > len(first_themes) * 0.7:
                patterns.append("Circular narrative structure")

        # Check for parallel storylines
        character_scenes = {}
        for node in nodes:
            for char in node.characters_present:
                if char not in character_scenes:
                    character_scenes[char] = []
                character_scenes[char].append(node.id)

        parallel_chars = [
            (char1, char2)
            for char1, scenes1 in character_scenes.items()
            for char2, scenes2 in character_scenes.items()
            if char1 < char2 and len(set(scenes1) & set(scenes2)) == 0
        ]

        if parallel_chars:
            patterns.append(f"Parallel storylines: {len(parallel_chars)} pairs")

        return patterns