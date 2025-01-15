"""Narrative Ontology System for mapping deep structural relationships in stories"""
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple
from enum import Enum
from .story_types import TimelineNode, CharacterAction
from .archetypal_patterns import ArchetypalPattern, NarrativeExcavator
import logging

logger = logging.getLogger(__name__)

class FryeMythos(Enum):
    """Northrop Frye's four mythoi"""
    COMEDY = "comedy"      # Spring myth
    ROMANCE = "romance"    # Summer myth
    TRAGEDY = "tragedy"    # Autumn myth
    IRONY = "irony"       # Winter myth

@dataclass
class FryeanPattern:
    """Patterns based on Northrop Frye's archetypal criticism"""
    mythos: FryeMythos
    phase: int  # 1-6 phases within each mythos
    character_types: Set[str]
    plot_movements: List[str]
    symbols: Set[str]
    thematic_elements: Set[str]
    typical_conflicts: List[Tuple[str, str]]
    resonance: float = 0.0  # How strongly this pattern is present

@dataclass
class CanonicalMapping:
    """Maps relationships to canonical source text"""
    source_text_id: str
    canonical_elements: Dict[str, float]
    thematic_fidelity: float
    structural_resonance: float
    divergent_elements: List[Dict[str, any]]
    frye_patterns: List[FryeanPattern] = field(default_factory=list)
    melville_resonance: float = 1.0

@dataclass
class NarrativeElement:
    """Fundamental unit in the narrative ontology"""
    id: str
    type: str
    name: str
    attributes: Dict[str, float]
    relationships: Dict[str, float]
    archetypal_resonance: Dict[str, float]
    variations: List[Dict[str, any]]
    canonical_source: Optional[str] = None
    melville_markers: Dict[str, float] = field(default_factory=dict)
    frye_categorization: Optional[FryeMythos] = None

class NarrativeOntologyBuilder:
    """System for building and analyzing narrative ontologies"""

    def __init__(self):
        self.elements: Dict[str, NarrativeElement] = {}
        self.mappings: Dict[str, CanonicalMapping] = {}
        self.excavator = NarrativeExcavator()
        self.canonical_patterns = {}
        self.variant_patterns = {}
        self.frye_patterns: Dict[FryeMythos, List[FryeanPattern]] = self._initialize_frye_patterns()

        # Initialize Melville's works patterns
        self.melville_works = {
            "moby_dick": {
                "themes": {"obsession", "isolation", "nature", "faith", "revenge"},
                "symbols": {"whale", "sea", "whiteness", "ship"},
                "character_types": {"monomaniac", "isolato", "prophet"},
                "frye_mythos": FryeMythos.TRAGEDY
            },
            "billy_budd": {
                "themes": {"innocence", "authority", "duty", "moral_ambiguity"},
                "symbols": {"handsome_sailor", "mutiny", "law", "hanging"},
                "character_types": {"innocent", "authority_figure", "tragic_witness"},
                "frye_mythos": FryeMythos.TRAGEDY
            },
            "bartleby": {
                "themes": {"resistance", "alienation", "capitalism", "humanity"},
                "symbols": {"wall", "office", "dead_letters", "preference"},
                "character_types": {"passive_resister", "corporate_figure", "observer"},
                "frye_mythos": FryeMythos.IRONY
            }
        }

    def _initialize_frye_patterns(self) -> Dict[FryeMythos, List[FryeanPattern]]:
        """Initialize Frye's archetypal patterns"""
        patterns = {mythos: [] for mythos in FryeMythos}

        # Comedy (Spring) patterns
        patterns[FryeMythos.COMEDY] = [
            FryeanPattern(
                mythos=FryeMythos.COMEDY,
                phase=1,
                character_types={"young lover", "blocking figure", "helper"},
                plot_movements=["obstacles to union", "recognition", "festive conclusion"],
                symbols={"spring", "garden", "festival", "marriage"},
                thematic_elements={"renewal", "reconciliation", "harmony"},
                typical_conflicts=[("youth", "age"), ("freedom", "society")]
            ),
            # Add more phases...
        ]

        # Romance (Summer) patterns
        patterns[FryeMythos.ROMANCE] = [
            FryeanPattern(
                mythos=FryeMythos.ROMANCE,
                phase=1,
                character_types={"hero", "companion", "antagonist"},
                plot_movements=["quest", "journey", "triumph"],
                symbols={"sword", "holy grail", "magical weapon"},
                thematic_elements={"adventure", "idealism", "victory"},
                typical_conflicts=[("good", "evil"), ("order", "chaos")]
            ),
            # Add more phases...
        ]

        # Tragedy (Autumn) patterns
        patterns[FryeMythos.TRAGEDY] = [
            FryeanPattern(
                mythos=FryeMythos.TRAGEDY,
                phase=1,
                character_types={"tragic hero", "nemesis", "chorus"},
                plot_movements=["hubris", "fall", "recognition"],
                symbols={"autumn", "sunset", "storm"},
                thematic_elements={"fate", "pride", "justice"},
                typical_conflicts=[("individual", "fate"), ("ambition", "limitation")]
            ),
            # Add more phases...
        ]

        # Irony/Satire (Winter) patterns
        patterns[FryeMythos.IRONY] = [
            FryeanPattern(
                mythos=FryeMythos.IRONY,
                phase=1,
                character_types={"anti-hero", "victim", "society"},
                plot_movements=["alienation", "absurdity", "cyclic return"],
                symbols={"winter", "darkness", "maze"},
                thematic_elements={"disillusionment", "absurdity", "limitation"},
                typical_conflicts=[("illusion", "reality"), ("individual", "society")]
            ),
            # Add more phases...
        ]

        return patterns

    def analyze_variant(self, 
                       variant_nodes: List[TimelineNode], 
                       variant_id: str,
                       canonical_id: str = "moby_dick_original") -> CanonicalMapping:
        """Analyze a variant version and map it to the canonical text"""
        try:
            # Extract narrative elements
            elements = self._extract_narrative_elements(variant_nodes)

            # Analyze Frye's patterns
            frye_analysis = self._analyze_frye_patterns(variant_nodes)

            # Map to canonical elements
            mapping = self._create_ontological_mapping(
                canonical_id=canonical_id,
                variant_id=variant_id,
                variant_elements=elements
            )

            # Analyze Melville-specific patterns
            melville_resonance = self._analyze_melville_resonance(variant_nodes)

            # Calculate archetypal shifts from canonical
            archetypal_shifts = self._calculate_archetypal_shifts(
                canonical_id=canonical_id,
                variant_patterns=self.excavator.excavate_patterns(variant_nodes)
            )

            # Calculate overall canonical fidelity
            canonical_fidelity = self._calculate_canonical_fidelity(
                mapping.element_mappings,
                archetypal_shifts,
                melville_resonance
            )

            mapping.archetypal_shifts = archetypal_shifts
            mapping.canonical_fidelity = canonical_fidelity
            mapping.frye_patterns = frye_analysis
            self.mappings[variant_id] = mapping

            logger.info(f"Completed ontological analysis of variant {variant_id}")
            return mapping

        except Exception as e:
            logger.error(f"Error analyzing variant: {str(e)}")
            raise

    def _analyze_frye_patterns(self, nodes: List[TimelineNode]) -> List[FryeanPattern]:
        """Analyze the presence of Frye's archetypal patterns in the narrative"""
        try:
            active_patterns = []

            # Analyze each mythos
            for mythos, patterns in self.frye_patterns.items():
                for pattern in patterns:
                    resonance = self._calculate_pattern_resonance(pattern, nodes)
                    if resonance > 0.3:  # Significant presence threshold
                        pattern_copy = FryeanPattern(
                            mythos=pattern.mythos,
                            phase=pattern.phase,
                            character_types=pattern.character_types.copy(),
                            plot_movements=pattern.plot_movements.copy(),
                            symbols=pattern.symbols.copy(),
                            thematic_elements=pattern.thematic_elements.copy(),
                            typical_conflicts=pattern.typical_conflicts.copy(),
                            resonance=resonance
                        )
                        active_patterns.append(pattern_copy)

            # Sort by resonance strength
            active_patterns.sort(key=lambda x: x.resonance, reverse=True)
            return active_patterns

        except Exception as e:
            logger.error(f"Error analyzing Frye patterns: {str(e)}")
            return []

    def _calculate_pattern_resonance(self, pattern: FryeanPattern, nodes: List[TimelineNode]) -> float:
        """Calculate how strongly a Frye pattern resonates in the narrative"""
        try:
            resonance_scores = []

            for node in nodes:
                # Check character types
                character_match = sum(1 for char_type in pattern.character_types
                                   if any(char_type.lower() in action.action_text.lower()
                                        for actions in node.character_actions.values()
                                        for action in actions))
                character_score = character_match / len(pattern.character_types) if pattern.character_types else 0

                # Check symbols
                symbol_match = sum(1 for symbol in pattern.symbols
                                 if symbol.lower() in node.description.lower())
                symbol_score = symbol_match / len(pattern.symbols) if pattern.symbols else 0

                # Check thematic elements
                theme_match = sum(1 for theme in pattern.thematic_elements
                                if theme in node.thematic_elements)
                theme_score = theme_match / len(pattern.thematic_elements) if pattern.thematic_elements else 0

                # Calculate node resonance
                node_resonance = (character_score * 0.4 + 
                                symbol_score * 0.3 + 
                                theme_score * 0.3)
                resonance_scores.append(node_resonance)

            # Return average resonance across all nodes
            return sum(resonance_scores) / len(resonance_scores) if resonance_scores else 0.0

        except Exception as e:
            logger.error(f"Error calculating pattern resonance: {str(e)}")
            return 0.0

    def _analyze_melville_resonance(self, nodes: List[TimelineNode]) -> float:
        """Analyze how strongly the narrative resonates with Melville's style"""
        try:
            total_resonance = 0.0
            weights = {"themes": 0.4, "symbols": 0.3, "character_types": 0.3}

            for node in nodes:
                # Check thematic alignment
                for work, patterns in self.melville_works.items():
                    theme_matches = sum(1 for theme in patterns["themes"] 
                                        if theme in node.thematic_elements)
                    symbol_matches = sum(1 for symbol in patterns["symbols"] 
                                         if symbol.lower() in node.description.lower())

                    # Character type analysis through actions and descriptions
                    char_type_matches = sum(1 for char_type in patterns["character_types"]
                                             if any(char_type.lower() in action.action_text.lower()
                                                  for actions in node.character_actions.values()
                                                  for action in actions))

                    work_resonance = (
                        theme_matches * weights["themes"] +
                        symbol_matches * weights["symbols"] +
                        char_type_matches * weights["character_types"]
                    ) / (len(patterns["themes"]) + len(patterns["symbols"]) + 
                         len(patterns["character_types"]))

                    total_resonance += work_resonance

            return min(total_resonance / len(self.melville_works), 1.0)

        except Exception as e:
            logger.error(f"Error analyzing Melville resonance: {str(e)}")
            return 0.0

    def _calculate_canonical_fidelity(self,
                                    element_mappings: Dict[str, Dict[str, float]],
                                    archetypal_shifts: Dict[str, float],
                                    melville_resonance: float) -> float:
        """Calculate how faithfully a variant follows the canonical text"""
        try:
            element_fidelity = sum(
                max(similarities.values()) if similarities else 0.0
                for similarities in element_mappings.values()
            ) / max(len(element_mappings), 1)

            pattern_fidelity = 1.0 - (sum(abs(shift) for shift in archetypal_shifts.values()) 
                                    / max(len(archetypal_shifts), 1))

            # Include Melville-specific resonance in fidelity calculation
            return (element_fidelity * 0.5 + 
                   pattern_fidelity * 0.2 + 
                   melville_resonance * 0.3)
        except Exception as e:
            logger.error(f"Error calculating canonical fidelity: {str(e)}")
            return 0.0

    def _extract_narrative_elements(self, nodes: List[TimelineNode]) -> Dict[str, NarrativeElement]:
        """Extract fundamental narrative elements from timeline nodes"""
        elements = {}

        for node in nodes:
            # Extract characters
            for char_id in node.characters_present:
                if char_id not in elements:
                    elements[char_id] = NarrativeElement(
                        id=char_id,
                        type="character",
                        name=char_id,  # Should be replaced with actual character name
                        attributes={},
                        relationships={},
                        archetypal_resonance={},
                        variations=[]
                    )

            # Extract locations
            location_id = f"location_{node.location}"
            if location_id not in elements:
                elements[location_id] = NarrativeElement(
                    id=location_id,
                    type="location",
                    name=node.location,
                    attributes={},
                    relationships={},
                    archetypal_resonance={},
                    variations=[]
                )

            # Extract themes
            for theme, strength in node.thematic_elements.items():
                theme_id = f"theme_{theme}"
                if theme_id not in elements:
                    elements[theme_id] = NarrativeElement(
                        id=theme_id,
                        type="theme",
                        name=theme,
                        attributes={"strength": strength},
                        relationships={},
                        archetypal_resonance={},
                        variations=[]
                    )

        return elements

    def _create_ontological_mapping(self,
                                  canonical_id: str,
                                  variant_id: str,
                                  variant_elements: Dict[str, NarrativeElement]) -> CanonicalMapping:
        """Create mapping between variant and canonical elements"""
        mapping = CanonicalMapping(
            base_text_id=canonical_id,
            variant_id=variant_id,
            element_mappings={},
            structural_similarities={},
            archetypal_shifts={}
        )

        # Map elements based on type and attributes
        for element_id, element in variant_elements.items():
            similarity_scores = self._calculate_element_similarities(element)
            mapping.element_mappings[element_id] = similarity_scores

        # Calculate structural similarities
        mapping.structural_similarities = self._calculate_structural_similarities(
            variant_elements=variant_elements,
            canonical_id=canonical_id
        )

        return mapping

    def _calculate_element_similarities(self, 
                                     element: NarrativeElement) -> Dict[str, float]:
        """Calculate similarity scores between a variant element and canonical elements"""
        similarities = {}

        # Compare with canonical elements of the same type
        for base_id, base_element in self.elements.items():
            if base_element.type == element.type:
                similarity = self._calculate_similarity_score(element, base_element)
                if similarity > 0.3:  # Only keep significant similarities
                    similarities[base_id] = similarity

        return similarities

    def _calculate_similarity_score(self,
                                  element_a: NarrativeElement,
                                  element_b: NarrativeElement) -> float:
        """Calculate similarity score between two narrative elements"""
        # Basic attribute comparison
        attribute_similarity = sum(
            min(element_a.attributes.get(attr, 0), element_b.attributes.get(attr, 0))
            for attr in set(element_a.attributes) & set(element_b.attributes)
        ) / max(len(element_a.attributes), len(element_b.attributes), 1)

        # Relationship pattern comparison
        relationship_similarity = sum(
            min(element_a.relationships.get(rel, 0), element_b.relationships.get(rel, 0))
            for rel in set(element_a.relationships) & set(element_b.relationships)
        ) / max(len(element_a.relationships), len(element_b.relationships), 1)

        # Archetypal resonance comparison
        resonance_similarity = sum(
            min(element_a.archetypal_resonance.get(pattern, 0), 
                element_b.archetypal_resonance.get(pattern, 0))
            for pattern in set(element_a.archetypal_resonance) & set(element_b.archetypal_resonance)
        ) / max(len(element_a.archetypal_resonance), len(element_b.archetypal_resonance), 1)

        return (attribute_similarity * 0.3 + 
                relationship_similarity * 0.4 + 
                resonance_similarity * 0.3)

    def _calculate_archetypal_shifts(self,
                                   canonical_id: str,
                                   variant_patterns: Dict[str, float]) -> Dict[str, float]:
        """Calculate how archetypal patterns have shifted from canonical text"""
        shifts = {}
        canonical_patterns = self.canonical_patterns.get(canonical_id, {})

        for pattern_id in set(canonical_patterns) | set(variant_patterns):
            canonical_strength = canonical_patterns.get(pattern_id, 0.0)
            variant_strength = variant_patterns.get(pattern_id, 0.0)
            shifts[pattern_id] = variant_strength - canonical_strength

        return shifts

    def register_canonical_text(self, text_id: str, nodes: List[TimelineNode]) -> None:
        """Register a canonical text as reference point"""
        try:
            # Extract and store canonical patterns
            self.canonical_patterns[text_id] = self.excavator.excavate_patterns(nodes)

            # Extract and store canonical elements
            canonical_elements = self._extract_narrative_elements(nodes)
            for element_id, element in canonical_elements.items():
                element.canonical_source = text_id
                self.elements[element_id] = element

            logger.info(f"Registered canonical text: {text_id}")

        except Exception as e:
            logger.error(f"Error registering canonical text: {str(e)}")
            raise

    def _calculate_structural_similarities(self,
                                        variant_elements: Dict[str, NarrativeElement],
                                        canonical_id: str) -> Dict[str, float]:
        """Calculate structural similarities between variant and base text"""
        similarities = {
            "character_network": self._compare_character_networks(variant_elements),
            "thematic_structure": self._compare_thematic_structures(variant_elements),
            "narrative_progression": self._compare_narrative_progressions(variant_elements)
        }
        return similarities
        
    def _compare_character_networks(self,
                                  variant_elements: Dict[str, NarrativeElement]) -> float:
        """Compare character relationship networks"""
        # Placeholder - implement network analysis
        return 0.5
        
    def _compare_thematic_structures(self,
                                   variant_elements: Dict[str, NarrativeElement]) -> float:
        """Compare thematic structures"""
        # Placeholder - implement thematic comparison
        return 0.5
        
    def _compare_narrative_progressions(self,
                                      variant_elements: Dict[str, NarrativeElement]) -> float:
        """Compare narrative progression patterns"""
        # Placeholder - implement progression analysis
        return 0.5

@dataclass
class OntologicalMapping:
    """Maps relationships between narrative elements across versions"""
    base_text_id: str  # Original/canonical text
    variant_id: str
    element_mappings: Dict[str, Dict[str, float]]  # base_element_id -> {variant_element_id: similarity}
    structural_similarities: Dict[str, float]  # Measures different aspects of similarity
    archetypal_shifts: Dict[str, float]  # How archetypal patterns have shifted
    canonical_fidelity: float = 1.0  # How closely variant follows canonical