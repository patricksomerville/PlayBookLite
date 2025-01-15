"""Author analysis module for gathering and analyzing literary patterns"""
import logging
from typing import Dict, List, Optional
import trafilatura
from urllib.parse import quote
import json

logger = logging.getLogger(__name__)

class AuthorAnalyzer:
    """Analyzes author's works to inform narrative ontology"""

    def __init__(self):
        self.cached_texts: Dict[str, str] = {}
        self.thematic_patterns: Dict[str, List[Dict[str, float]]] = {}
        self.structural_elements: Dict[str, List[str]] = {}

    def analyze_author_works(self, author_name: str, work_urls: List[str]) -> Dict:
        """Analyze patterns across an author's works"""
        try:
            results = {
                "author": author_name,
                "works_analyzed": [],
                "recurring_themes": {},
                "narrative_techniques": [],
                "character_archetypes": []
            }

            for url in work_urls:
                try:
                    # Extract text content
                    downloaded = trafilatura.fetch_url(url)
                    if downloaded:
                        text = trafilatura.extract(downloaded)
                        if text:
                            self.cached_texts[url] = text

                            # Analyze work
                            work_analysis = self._analyze_single_work(text)
                            results["works_analyzed"].append({
                                "url": url,
                                "themes": work_analysis.get("themes", []),
                                "techniques": work_analysis.get("techniques", [])
                            })

                            # Update overall patterns
                            self._update_thematic_patterns(work_analysis.get("themes", []))

                except Exception as e:
                    logger.error(f"Error analyzing work at {url}: {str(e)}")
                    continue

            # Aggregate patterns across works
            results["recurring_themes"] = self._get_recurring_themes()
            results["narrative_techniques"] = self._get_common_techniques()

            return results

        except Exception as e:
            logger.error(f"Error in author analysis: {str(e)}")
            return {}

    def _analyze_single_work(self, text: str) -> Dict:
        """Analyze patterns in a single work"""
        try:
            analysis = {
                "themes": [],
                "techniques": [],
                "character_types": []
            }

            # Extract key themes from text
            # This would be enhanced with more sophisticated NLP analysis
            potential_themes = [
                "identity", "memory", "time", "connection",
                "technology", "loss", "redemption", "family",
                "consciousness", "reality", "perception"
            ]

            for theme in potential_themes:
                if theme.lower() in text.lower():
                    theme_strength = text.lower().count(theme.lower()) / len(text.split())
                    analysis["themes"].append({
                        "name": theme,
                        "strength": min(theme_strength * 1000, 1.0)  # Normalize to 0-1
                    })

            # Analyze narrative techniques
            if "flashback" in text.lower() or "remembered" in text.lower():
                analysis["techniques"].append("non_linear_narrative")
            if "thought" in text.lower() or "felt" in text.lower():
                analysis["techniques"].append("internal_monologue")

            return analysis

        except Exception as e:
            logger.error(f"Error analyzing single work: {str(e)}")
            return {}

    def _update_thematic_patterns(self, themes: List[Dict[str, float]]) -> None:
        """Update running analysis of thematic patterns"""
        for theme in themes:
            theme_name = theme.get("name")
            if theme_name:
                if theme_name not in self.thematic_patterns:
                    self.thematic_patterns[theme_name] = []
                self.thematic_patterns[theme_name].append(theme.get("strength", 0.5))

    def _get_recurring_themes(self) -> Dict[str, float]:
        """Get themes that recur across works"""
        recurring = {}
        for theme, strengths in self.thematic_patterns.items():
            if len(strengths) > 1:  # Theme appears in multiple works
                avg_strength = sum(strengths) / len(strengths)
                recurring[theme] = avg_strength
        return recurring

    def _get_common_techniques(self) -> List[str]:
        """Get narrative techniques used across works"""
        return list(self.structural_elements.keys())

    def export_analysis(self, filepath: str) -> None:
        """Export analysis results to JSON"""
        try:
            analysis = {
                "thematic_patterns": self.thematic_patterns,
                "structural_elements": self.structural_elements
            }
            with open(filepath, 'w') as f:
                json.dump(analysis, f, indent=2)
        except Exception as e:
            logger.error(f"Error exporting analysis: {str(e)}")