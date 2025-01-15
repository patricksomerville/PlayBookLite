"""Content Generator: Uses OpenAI to generate authentic persona content."""

import os
import logging
from typing import Dict, Any, List, Optional
from openai import OpenAI
from datetime import datetime

class ContentGenerator:
    """Generates authentic content for literary personas using OpenAI."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Initialize OpenAI client
        openai_key = os.getenv('OPENAI_API_KEY')
        if not openai_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=openai_key)
        
        # Load persona characteristics
        self.persona_voices = {
            "mary_shelley": {
                "voice": "Gothic, scientific, feminist",
                "themes": ["scientific ambition", "female autonomy", "loss", "creation"],
                "style": "Philosophical and emotional, with Gothic undertones",
                "relationships": {
                    "percy_shelley": "husband and intellectual partner",
                    "lord_byron": "complicated friend and fellow writer"
                }
            },
            "lord_byron": {
                "voice": "Witty, passionate, aristocratic",
                "themes": ["desire", "exile", "social critique", "male beauty"],
                "style": "Satirical yet romantic, with dark undertones",
                "relationships": {
                    "percy_shelley": "intimate friend and fellow poet",
                    "mary_shelley": "intellectual companion"
                }
            },
            "percy_shelley": {
                "voice": "Lyrical, revolutionary, passionate",
                "themes": ["love", "political revolution", "nature", "freedom"],
                "style": "Ethereal and idealistic, with revolutionary fervor",
                "relationships": {
                    "mary_shelley": "wife and intellectual equal",
                    "lord_byron": "close friend and poetic inspiration"
                }
            },
            "herman_melville": {
                "voice": "Philosophical, coded, observant",
                "themes": ["male intimacy", "societal constraints", "truth-seeking"],
                "style": "Dense prose with layered meanings and maritime metaphors",
                "relationships": {
                    "nathaniel_hawthorne": "profound intellectual and emotional connection"
                }
            }
        }

    def generate_diary_entry(self, persona: str, context: Dict[str, Any]) -> str:
        """Generate a private diary entry."""
        voice = self.persona_voices[persona]
        
        prompt = f"""You are {persona}, writing a private diary entry. Write in first person.

Your voice is {voice['voice']}.
Your common themes are: {', '.join(voice['themes'])}.
Your writing style is: {voice['style']}.

Context for this entry:
- Current mood: {context.get('mood', 'contemplative')}
- Location: {context.get('location', 'private chamber')}
- Recent events: {context.get('recent_events', 'a day of writing and reflection')}

Write an intimate diary entry expressing your private thoughts and feelings. Include:
1. Personal reflections on your relationships and desires
2. Hidden meanings and coded language about forbidden topics
3. Your true feelings about society's constraints
4. References to your current creative work

Write in a deeply personal, unguarded style as this is for your private diary."""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1000
        )
        
        return response.choices[0].message.content

    def generate_intimate_letter(self, 
                               sender: str, 
                               recipient: str, 
                               context: Dict[str, Any]) -> str:
        """Generate an intimate letter between personas."""
        sender_voice = self.persona_voices[sender]
        relationship = sender_voice["relationships"].get(recipient, "fellow writer")
        
        prompt = f"""You are {sender}, writing an intimate letter to {recipient}, your {relationship}.
Write in first person, addressing {recipient} directly.

Your voice is {sender_voice['voice']}.
Your writing style is {sender_voice['style']}.

Context for this letter:
- Your mood: {context.get('mood', 'yearning')}
- Location: {context.get('location', 'private chamber')}
- Recent interaction: {context.get('recent_interaction', 'a meaningful conversation')}

Write a deeply personal letter that:
1. Expresses your true feelings using period-appropriate coded language
2. References shared intellectual and emotional connections
3. Discusses your private thoughts about society's constraints
4. Includes subtle references to your intimate relationship
5. Mentions your creative work and shared inspirations

Write with both passion and restraint, using metaphor and allusion to convey deeper meanings."""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1200
        )
        
        return response.choices[0].message.content

    def generate_private_poem(self, persona: str, theme: str) -> str:
        """Generate a private poem exploring intimate themes."""
        voice = self.persona_voices[persona]
        
        prompt = f"""You are {persona}, writing a private poem not intended for publication.
Write in your authentic voice, which is {voice['voice']}.

Theme to explore: {theme}

Your writing style is {voice['style']}.
Include references to your common themes: {', '.join(voice['themes'])}.

Create a poem that:
1. Explores forbidden desires and hidden feelings
2. Uses natural or classical imagery as metaphor
3. Challenges societal constraints through coded language
4. Expresses authentic emotional and physical desire
5. Maintains plausible deniability through metaphor

Write with both passion and craft, knowing this is for your private collection."""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=800
        )
        
        return response.choices[0].message.content

    def generate_intimate_dialogue(self, 
                                 participants: List[str], 
                                 setting: str) -> str:
        """Generate an intimate conversation between personas."""
        participant_voices = {p: self.persona_voices[p] for p in participants}
        
        prompt = f"""Generate an intimate conversation between {', '.join(participants)}.

Setting: {setting}

Character voices:
{chr(10).join(f'- {p}: {v["voice"]}' for p, v in participant_voices.items())}

Relationships:
"""
        # Add relationship context
        for p1 in participants:
            for p2 in participants:
                if p1 != p2 and p2 in self.persona_voices[p1]["relationships"]:
                    prompt += f"- {p1} and {p2}: {self.persona_voices[p1]['relationships'][p2]}\n"

        prompt += """
Create a conversation that:
1. Maintains each person's distinct voice and perspective
2. Includes subtle references to their intimate relationships
3. Uses period-appropriate coded language for forbidden topics
4. Weaves in their shared intellectual and creative interests
5. Shows both spoken dialogue and unspoken tensions

Write the conversation as a natural flow of dialogue with minimal narrative interruption."""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1500
        )
        
        return response.choices[0].message.content

    def generate_unfinished_work(self, 
                                persona: str, 
                                work_type: str,
                                context: Dict[str, Any]) -> str:
        """Generate an unfinished creative work with personal significance."""
        voice = self.persona_voices[persona]
        
        prompt = f"""You are {persona}, working on a private {work_type} that may never be published.
Write in your authentic voice, which is {voice['voice']}.

Context:
- Current inspiration: {context.get('inspiration', 'personal experience')}
- Emotional state: {context.get('mood', 'introspective')}
- Private meaning: {context.get('private_meaning', 'exploration of forbidden themes')}

Your writing style is {voice['style']}.
Your common themes include: {', '.join(voice['themes'])}.

Create an unfinished work that:
1. Explores your private thoughts and feelings through metaphor
2. Uses coded language to discuss forbidden topics
3. Weaves in autobiographical elements disguised as fiction
4. Challenges societal constraints through allegory
5. Contains personal references that only intimate friends would understand

Write this as a work in progress, with the raw honesty of something not meant for public eyes."""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
