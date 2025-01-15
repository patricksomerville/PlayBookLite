"""Archetypal pattern recognition and narrative excavation system"""
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
import logging
from .story_types import TimelineNode, CharacterAction, StoryState

logger = logging.getLogger(__name__)

@dataclass
class ArchetypalPattern:
    """Represents a fundamental narrative pattern"""
    name: str
    core_themes: Set[str]
    character_roles: Dict[str, str]  # character_id -> archetypal role
    symbolic_elements: Dict[str, float]  # symbol -> resonance strength
    narrative_tensions: List[Tuple[str, str]]  # pairs of opposing forces

class NarrativeExcavator:
    """System for uncovering inherent narrative patterns and archetypal structures"""

    def __init__(self):
        self.archetypal_patterns = {
            "hero_journey": ArchetypalPattern(
                name="The Hero's Journey",
                core_themes={"transformation", "return", "sacrifice"},
                character_roles={
                    "mentor": "guide",
                    "shadow": "challenger",
                    "threshold_guardian": "gatekeeper"
                },
                symbolic_elements={
                    "crossing_threshold": 0.8,
                    "descent": 0.7,
                    "rebirth": 0.9
                },
                narrative_tensions=[
                    ("ordinary", "extraordinary"),
                    ("fear", "courage"),
                    ("death", "rebirth")
                ]
            ),
            "tragic_fall": ArchetypalPattern(
                name="Tragic Fall",
                core_themes={"hubris", "nemesis", "recognition"},
                character_roles={
                    "tragic_hero": "protagonist",
                    "nemesis": "antagonist",
                    "chorus": "witness"
                },
                symbolic_elements={
                    "fatal_flaw": 0.9,
                    "prophecy": 0.7,
                    "recognition": 0.8
                },
                narrative_tensions=[
                    ("pride", "fall"),
                    ("destiny", "free_will"),
                    ("knowledge", "ignorance")
                ]
            ),
            "rebirth": ArchetypalPattern(
                name="Rebirth",
                core_themes={"redemption", "forgiveness", "renewal"},
                character_roles={
                    "fallen_hero": "protagonist",
                    "catalyst": "guide",
                    "witness": "observer"
                },
                symbolic_elements={
                    "darkness": 0.8,
                    "light": 0.8,
                    "water": 0.7,
                    "spring": 0.6
                },
                narrative_tensions=[
                    ("sin", "redemption"),
                    ("isolation", "connection"),
                    ("past", "future")
                ]
            ),
            "quest": ArchetypalPattern(
                name="The Quest",
                core_themes={"seeking", "discovery", "trial"},
                character_roles={
                    "seeker": "protagonist",
                    "helper": "ally",
                    "adversary": "challenger"
                },
                symbolic_elements={
                    "journey": 0.9,
                    "artifact": 0.8,
                    "obstacle": 0.7
                },
                narrative_tensions=[
                    ("ignorance", "wisdom"),
                    ("weakness", "strength"),
                    ("doubt", "faith")
                ]
            )
        }

        self.active_patterns: Dict[str, float] = {}  # pattern_id -> resonance_strength
        self.symbolic_depth: Dict[str, List[float]] = {}  # symbol -> depth_measurements
        self.thematic_layers: List[Dict[str, float]] = []  # temporal layers of theme strength

    def excavate_patterns(self, timeline_nodes: List[TimelineNode]) -> Dict[str, float]:
        """Uncover archetypal patterns present in the narrative structure"""
        try:
            pattern_resonance = {}

            for pattern_id, pattern in self.archetypal_patterns.items():
                resonance = self._measure_pattern_resonance(pattern, timeline_nodes)
                if resonance > 0.4:  # Significant resonance threshold
                    pattern_resonance[pattern_id] = resonance
                    logger.info(f"Found archetypal pattern: {pattern_id} with resonance {resonance:.2f}")

            return pattern_resonance

        except Exception as e:
            logger.error(f"Error excavating patterns: {str(e)}")
            return {}

    def _measure_pattern_resonance(self, pattern: ArchetypalPattern, nodes: List[TimelineNode]) -> float:
        """Measure how strongly a pattern resonates in the narrative"""
        try:
            theme_resonance = self._calculate_thematic_resonance(pattern.core_themes, nodes)
            symbol_resonance = self._calculate_symbolic_resonance(pattern.symbolic_elements, nodes)
            tension_resonance = self._calculate_tension_resonance(pattern.narrative_tensions, nodes)

            # Weight the different types of resonance
            return (theme_resonance * 0.4 + 
                   symbol_resonance * 0.3 + 
                   tension_resonance * 0.3)

        except Exception as e:
            logger.error(f"Error measuring pattern resonance: {str(e)}")
            return 0.0

    def _calculate_thematic_resonance(self, core_themes: Set[str], nodes: List[TimelineNode]) -> float:
        """Calculate how strongly the core themes resonate through the narrative"""
        try:
            if not nodes:
                return 0.0

            total_resonance = 0.0
            for theme in core_themes:
                theme_presence = sum(
                    node.thematic_elements.get(theme, 0.0) for node in nodes
                ) / len(nodes)
                total_resonance += theme_presence

            return total_resonance / len(core_themes) if core_themes else 0.0

        except Exception as e:
            logger.error(f"Error calculating thematic resonance: {str(e)}")
            return 0.0

    def _calculate_symbolic_resonance(self, symbols: Dict[str, float], nodes: List[TimelineNode]) -> float:
        """Calculate the resonance of symbolic elements throughout the narrative"""
        try:
            if not nodes or not symbols:
                return 0.0

            total_resonance = 0.0
            for symbol, base_strength in symbols.items():
                # Look for symbolic elements in node descriptions and actions
                symbol_presence = sum(
                    1 for node in nodes
                    if symbol.lower() in node.description.lower()
                    or any(symbol.lower() in action.action_text.lower() 
                          for actions in node.character_actions.values()
                          for action in actions)
                ) / len(nodes)

                total_resonance += symbol_presence * base_strength

            return total_resonance / len(symbols) if symbols else 0.0

        except Exception as e:
            logger.error(f"Error calculating symbolic resonance: {str(e)}")
            return 0.0

    def _calculate_tension_resonance(self, tensions: List[Tuple[str, str]], nodes: List[TimelineNode]) -> float:
        """Calculate the resonance of narrative tensions through the story"""
        try:
            if not nodes or not tensions:
                return 0.0

            total_resonance = 0.0
            for opposing_force_a, opposing_force_b in tensions:
                # Look for tension pairs in node descriptions and thematic elements
                tension_presence = sum(
                    1 for node in nodes
                    if (opposing_force_a.lower() in node.description.lower() 
                        and opposing_force_b.lower() in node.description.lower())
                    or (node.thematic_elements.get(opposing_force_a, 0.0) > 0.3
                        and node.thematic_elements.get(opposing_force_b, 0.0) > 0.3)
                ) / len(nodes)

                total_resonance += tension_presence

            return total_resonance / len(tensions) if tensions else 0.0

        except Exception as e:
            logger.error(f"Error calculating tension resonance: {str(e)}")
            return 0.0

    def analyze_narrative_depth(self, nodes: List[TimelineNode]) -> Dict[str, List[float]]:
        """Analyze the depth of narrative elements across different layers"""
        depths = {}
        try:
            if not nodes:
                return depths

            # Analyze symbolic depth
            for node in nodes:
                for symbol in self._extract_symbols(node):
                    if symbol not in depths:
                        depths[symbol] = []
                    depth = self._calculate_symbol_depth(symbol, node)
                    depths[symbol].append(depth)

            # Record the analysis
            self.symbolic_depth = depths
            logger.info(f"Analyzed narrative depth across {len(nodes)} nodes")

            return depths

        except Exception as e:
            logger.error(f"Error analyzing narrative depth: {str(e)}")
            return {}

    def _extract_symbols(self, node: TimelineNode) -> Set[str]:
        """Extract symbolic elements from a timeline node"""
        symbols = set()
        try:
            # Extract from description
            words = node.description.lower().split()
            for word in words:
                for pattern in self.archetypal_patterns.values():
                    if word in pattern.symbolic_elements:
                        symbols.add(word)

            # Extract from character actions
            for actions in node.character_actions.values():
                for action in actions:
                    action_words = action.action_text.lower().split()
                    for word in action_words:
                        for pattern in self.archetypal_patterns.values():
                            if word in pattern.symbolic_elements:
                                symbols.add(word)

            # Extract from thematic elements
            for theme in node.thematic_elements:
                theme_word = theme.lower()
                for pattern in self.archetypal_patterns.values():
                    if theme_word in pattern.symbolic_elements:
                        symbols.add(theme_word)

            return symbols

        except Exception as e:
            logger.error(f"Error extracting symbols: {str(e)}")
            return set()

    def _calculate_symbol_depth(self, symbol: str, node: TimelineNode) -> float:
        """Calculate the depth of a symbolic element in a given node"""
        try:
            depth = 0.0

            # Base depth on frequency
            if symbol.lower() in node.description.lower():
                depth += 0.3

            # Connection to character arcs
            for actions in node.character_actions.values():
                for action in actions:
                    if symbol.lower() in action.action_text.lower():
                        depth += 0.2

            # Relation to thematic elements
            for theme, strength in node.thematic_elements.items():
                if symbol.lower() in theme.lower():
                    depth += strength * 0.3

            # Integration with tensions
            tension_integration = 0.0
            for actions in node.character_actions.values():
                for action in actions:
                    if symbol.lower() in action.action_text.lower():
                        tension_integration += action.impact_level * 0.2

            depth += tension_integration
            return min(depth, 1.0)  # Normalize to 0-1 range

        except Exception as e:
            logger.error(f"Error calculating symbol depth: {str(e)}")
            return 0.0

    def get_narrative_layers(self) -> List[Dict[str, float]]:
        """Get the analyzed thematic layers of the narrative"""
        return self.thematic_layers