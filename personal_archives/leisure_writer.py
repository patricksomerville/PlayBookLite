"""Leisure Writer: Manages the personas' private writing activities during their spare time."""

import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from .archive_manager import ArchiveManager

class LeisureWriter:
    """Manages and generates private writings for literary personas during their leisure time."""
    
    def __init__(self, archive_manager: ArchiveManager):
        self.logger = logging.getLogger(__name__)
        self.archive_manager = archive_manager
        
        # Track writing sessions and relationships
        self.active_sessions = {}
        self.relationships = {
            "mary_shelley": {
                "primary_connections": ["percy_shelley", "lord_byron"],
                "interests": ["gothic horror", "science", "mortality", "female autonomy"]
            },
            "lord_byron": {
                "primary_connections": ["percy_shelley", "mary_shelley"],
                "interests": ["passion", "exile", "social critique", "male beauty"]
            },
            "percy_shelley": {
                "primary_connections": ["mary_shelley", "lord_byron"],
                "interests": ["radical politics", "nature", "love", "revolution"]
            },
            "herman_melville": {
                "primary_connections": ["nathaniel_hawthorne"],
                "interests": ["male intimacy", "metaphysics", "nature", "social constraints"]
            }
        }
        
        # Initialize writing prompts for each category
        self.writing_prompts = {
            "diary_entries": [
                "Reflecting on today's intimate conversations",
                "Thoughts on societal constraints and personal freedom",
                "Observations of natural beauty and hidden meanings",
                "Meditations on love, desire, and connection"
            ],
            "letters": [
                "Expressing deep admiration and intellectual connection",
                "Sharing private thoughts and coded messages",
                "Discussing literary works and their hidden meanings",
                "Planning future meetings and shared experiences"
            ],
            "private_poems": [
                "Odes to forbidden love and desire",
                "Nature as metaphor for human connection",
                "The pain of societal constraints",
                "Celebrations of beauty and passion"
            ],
            "intimate_thoughts": [
                "Personal struggles with identity and desire",
                "Dreams and visions of freedom",
                "Reflections on meaningful encounters",
                "Hopes for future understanding"
            ]
        }
    
    def generate_leisure_writing(self, 
                               persona: str, 
                               category: str,
                               prompt: Optional[str] = None) -> Dict[str, Any]:
        """Generate a new piece of private writing for a persona."""
        try:
            # Use provided prompt or select a random one
            if not prompt:
                prompt = self._select_prompt(category)
            
            # Get the persona's current context
            context = self._get_persona_context(persona)
            
            # Generate the content (this would typically use the persona's API)
            # For now, we'll use a placeholder
            content = f"[Generated content for {persona} based on prompt: {prompt}]"
            
            # Prepare metadata
            metadata = {
                "title": f"{prompt.split()[0]}...",
                "prompt": prompt,
                "mood": context.get("mood", "contemplative"),
                "location": context.get("location", "private chamber"),
                "tags": self.relationships[persona]["interests"][:2]
            }
            
            # Store the writing
            filename = self.archive_manager.store_writing(
                persona=persona,
                category=category,
                content=content,
                metadata=metadata
            )
            
            return {
                "status": "success",
                "filename": filename,
                "content": content,
                "metadata": metadata
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate leisure writing: {str(e)}")
            raise
    
    def generate_intimate_interaction(self, 
                                    initiator: str, 
                                    recipient: str) -> Dict[str, Any]:
        """Generate an intimate interaction between two personas."""
        try:
            if recipient not in self.relationships[initiator]["primary_connections"]:
                raise ValueError(f"No established intimate connection between {initiator} and {recipient}")
            
            # Generate the interaction content (would typically use personas' APIs)
            content = f"[Generated intimate interaction between {initiator} and {recipient}]"
            
            # Prepare metadata
            metadata = {
                "location": "private salon",
                "mood": "intimate",
                "context": "leisure time",
                "type": "private conversation"
            }
            
            # Store the interaction
            stored_files = self.archive_manager.store_interaction(
                participants=[initiator, recipient],
                interaction_type="intimate_conversation",
                content=content,
                metadata=metadata
            )
            
            return {
                "status": "success",
                "files": stored_files,
                "content": content,
                "metadata": metadata
            }
            
        except Exception as e:
            self.logger.error(f"Failed to generate intimate interaction: {str(e)}")
            raise
    
    def _select_prompt(self, category: str) -> str:
        """Select a writing prompt for the given category."""
        import random
        return random.choice(self.writing_prompts[category])
    
    def _get_persona_context(self, persona: str) -> Dict[str, Any]:
        """Get the current context for a persona."""
        # This would typically involve checking the persona's current state
        # For now, return a simple context
        return {
            "mood": "contemplative",
            "location": "private chamber",
            "time_of_day": "evening"
        }
