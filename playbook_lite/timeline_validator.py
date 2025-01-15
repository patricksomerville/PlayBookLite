"""Timeline consistency validation for character-driven narrative excavation"""
import logging
from typing import Dict, List, Set, Tuple, Optional
from playbook_lite.story_types import TimelineNode, CharacterAction, StoryState
from playbook_lite.archetypal_patterns import NarrativeExcavator
from playbook_lite.narrative_ontology import NarrativeOntologyBuilder

logger = logging.getLogger(__name__)

class TimelineConsistencyValidator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.canonical_nodes: Set[str] = set()
        self.character_actions: Dict[str, List[CharacterAction]] = {}
        self.excavator = NarrativeExcavator()
        self.ontology_builder = NarrativeOntologyBuilder()
        self.thematic_weights = {
            "revenge": 0.8,
            "obsession": 0.9,
            "isolation": 0.7,
            "friendship": 0.6,
            "fate": 0.8,
            "nature": 0.7
        }
        self.active_patterns = {}
        self.narrative_depth = {}
        self.current_variant_id = None

    def set_variant_id(self, variant_id: str) -> None:
        """Set the current variant ID for ontological tracking"""
        self.current_variant_id = variant_id

    def validate_story_progression(self, current_state: Optional[StoryState], next_node: TimelineNode) -> Tuple[bool, float, str]:
        """Validate if the story can progress to the next node while maintaining archetypal consistency"""
        try:
            if current_state is None:
                return False, 1.0, "Invalid state: Story state not initialized"

            # Check basic connectivity
            if not current_state.available_actions:
                return True, current_state.canonical_drift, "No actions available"

            if next_node.id not in current_state.available_actions[0].consequences:
                return False, 1.0, "Invalid story progression - nodes not connected"

            # Analyze archetypal patterns in the current narrative state
            if not self.active_patterns:
                all_nodes = [node for node in self._get_all_nodes()]  
                self.active_patterns = self.excavator.excavate_patterns(all_nodes)
                self.narrative_depth = self.excavator.analyze_narrative_depth(all_nodes)

                # Update ontological mapping if variant ID is set
                if self.current_variant_id:
                    self.ontology_builder.analyze_variant(
                        variant_nodes=all_nodes,
                        variant_id=self.current_variant_id
                    )

            # Calculate pattern resonance for the new node
            pattern_consistency = self._validate_pattern_consistency(current_state, next_node)
            if pattern_consistency < 0.4:
                return False, 1.0, "Progression breaks archetypal pattern consistency"

            # Calculate thematic drift while considering archetypal patterns
            thematic_drift = self._calculate_thematic_drift(
                current_state.active_themes,
                next_node.thematic_elements,
                self.active_patterns
            )

            # Update canonical drift based on chosen path and archetypal consistency
            new_canonical_drift = self._update_canonical_drift(
                current_state.canonical_drift,
                next_node.id in self.canonical_nodes,
                thematic_drift,
                pattern_consistency
            )

            # Determine if we're too far from canonical ending
            if new_canonical_drift > 0.8 and self._is_near_ending(next_node):
                return False, new_canonical_drift, "Story diverged too far from canonical ending"

            return True, new_canonical_drift, "Valid progression"

        except Exception as e:
            self.logger.error(f"Error validating story progression: {str(e)}")
            return False, 1.0, f"Validation error: {str(e)}"

    def register_canonical_action(self, character_id: str, action: CharacterAction) -> None:
        """Register a canonical character action from the original text"""
        try:
            if character_id not in self.character_actions:
                self.character_actions[character_id] = []
            self.character_actions[character_id].append(action)
            self.logger.info(f"Registered canonical action for {character_id}: {action.action_text}")
        except Exception as e:
            self.logger.error(f"Failed to register canonical action: {str(e)}")
            raise

    def validate_story_progression(self, current_state: Optional[StoryState], next_node: TimelineNode) -> Tuple[bool, float, str]:
        """Validate if the story can progress to the next node while maintaining archetypal consistency"""
        try:
            if current_state is None:
                return False, 1.0, "Invalid state: Story state not initialized"

            # Check basic connectivity
            if not current_state.available_actions:
                return True, current_state.canonical_drift, "No actions available"

            if next_node.id not in current_state.available_actions[0].consequences:
                return False, 1.0, "Invalid story progression - nodes not connected"

            # Analyze archetypal patterns in the current narrative state
            if not self.active_patterns:
                all_nodes = [node for node in self._get_all_nodes()]  
                self.active_patterns = self.excavator.excavate_patterns(all_nodes)
                self.narrative_depth = self.excavator.analyze_narrative_depth(all_nodes)

                # Update ontological mapping if variant ID is set
                if self.current_variant_id:
                    self.ontology_builder.analyze_variant(
                        variant_nodes=all_nodes,
                        variant_id=self.current_variant_id
                    )

            # Calculate pattern resonance for the new node
            pattern_consistency = self._validate_pattern_consistency(current_state, next_node)
            if pattern_consistency < 0.4:
                return False, 1.0, "Progression breaks archetypal pattern consistency"

            # Calculate thematic drift while considering archetypal patterns
            thematic_drift = self._calculate_thematic_drift(
                current_state.active_themes,
                next_node.thematic_elements,
                self.active_patterns
            )

            # Update canonical drift based on chosen path and archetypal consistency
            new_canonical_drift = self._update_canonical_drift(
                current_state.canonical_drift,
                next_node.id in self.canonical_nodes,
                thematic_drift,
                pattern_consistency
            )

            # Determine if we're too far from canonical ending
            if new_canonical_drift > 0.8 and self._is_near_ending(next_node):
                return False, new_canonical_drift, "Story diverged too far from canonical ending"

            return True, new_canonical_drift, "Valid progression"

        except Exception as e:
            self.logger.error(f"Error validating story progression: {str(e)}")
            return False, 1.0, f"Validation error: {str(e)}"

    def get_available_actions(self, character_id: str, story_state: Optional[StoryState]) -> List[CharacterAction]:
        """Get available actions for a character based on current story state"""
        try:
            if story_state is None:
                self.logger.warning("Story state not initialized when getting actions")
                return []

            if character_id not in self.character_actions:
                return []

            return [
                action for action in self.character_actions.get(character_id, [])
                if self._is_action_valid(action, story_state)
            ]
        except Exception as e:
            self.logger.error(f"Error getting available actions: {str(e)}")
            return []

    def _calculate_thematic_drift(self, current_themes: Dict[str, float], 
                                next_themes: Dict[str, float],
                                active_patterns: Dict[str, float]) -> float:
        """Calculate thematic drift while considering archetypal patterns"""
        try:
            total_drift = 0.0
            total_weight = 0.0

            # Consider both explicit themes and archetypal themes
            all_themes = set(current_themes.keys()) | set(next_themes.keys())
            for pattern_id, resonance in active_patterns.items():
                pattern = self.excavator.archetypal_patterns.get(pattern_id)
                if pattern:
                    all_themes.update(pattern.core_themes)

            for theme in all_themes:
                weight = self.thematic_weights.get(theme, 0.5)
                # Increase weight for themes that are part of active archetypal patterns
                for pattern_id, resonance in active_patterns.items():
                    pattern = self.excavator.archetypal_patterns.get(pattern_id)
                    if pattern and theme in pattern.core_themes:
                        weight *= (1 + resonance)

                current_value = current_themes.get(theme, 0.0)
                next_value = next_themes.get(theme, 0.0)
                drift = abs(current_value - next_value) * weight
                total_drift += drift
                total_weight += weight

            return total_drift / total_weight if total_weight > 0 else 0.0

        except Exception as e:
            self.logger.error(f"Error calculating thematic drift: {str(e)}")
            return 0.0

    def _update_canonical_drift(self, current_drift: float, 
                              is_canonical_node: bool, 
                              thematic_drift: float,
                              pattern_consistency: float) -> float:
        """Update canonical drift considering archetypal pattern consistency"""
        try:
            # Balance between canonical adherence and archetypal resonance
            drift_factor = 0.7 if is_canonical_node else 1.3
            pattern_factor = 1 - pattern_consistency  # Lower consistency increases drift

            new_drift = (current_drift * drift_factor * 0.4 + 
                        thematic_drift * 0.3 +
                        pattern_factor * 0.3)

            return min(max(new_drift, 0.0), 1.0)

        except Exception as e:
            self.logger.error(f"Error updating canonical drift: {str(e)}")
            return current_drift

    def _validate_pattern_consistency(self, current_state: StoryState, next_node: TimelineNode) -> float:
        """Validate how well the next node maintains archetypal pattern consistency"""
        try:
            if not self.active_patterns:
                return 1.0

            consistency_scores = []
            for pattern_id, resonance in self.active_patterns.items():
                pattern = self.excavator.archetypal_patterns.get(pattern_id)
                if pattern:
                    # Check thematic consistency
                    theme_match = sum(1 for theme in pattern.core_themes 
                                    if theme in next_node.thematic_elements)
                    theme_score = theme_match / len(pattern.core_themes) if pattern.core_themes else 1.0

                    # Check character role consistency
                    role_match = sum(1 for char_id in next_node.characters_present 
                                   if char_id in pattern.character_roles)
                    role_score = role_match / len(next_node.characters_present) if next_node.characters_present else 1.0

                    # Weight the scores by the pattern's resonance
                    consistency_scores.append((theme_score * 0.6 + role_score * 0.4) * resonance)

            return sum(consistency_scores) / len(consistency_scores) if consistency_scores else 1.0

        except Exception as e:
            self.logger.error(f"Error validating pattern consistency: {str(e)}")
            return 0.0


    def _is_near_ending(self, node: TimelineNode) -> bool:
        """Check if we're in the final 20% of the story"""
        return False  # To be implemented based on story progress tracking

    def _is_action_valid(self, action: CharacterAction, state: StoryState) -> bool:
        """Check if an action is valid given the current story state"""
        try:
            # Basic validation - action should be available and not conflict with current state
            if not action or not state:
                return False

            # Canonical actions are always valid early in the story
            if action.is_canonical and state.canonical_drift < 0.5:
                return True

            # Non-canonical actions become more available as we drift from canon
            return True  # Enhanced validation to be implemented
        except Exception as e:
            self.logger.error(f"Error validating action: {str(e)}")
            return False

    def _get_all_nodes(self):
        # Placeholder implementation - needs actual story node retrieval
        yield from [] # Replace with actual node retrieval logic