"""Archive Manager for storing and organizing personas' private writings."""

import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

class ArchiveManager:
    """Manages the storage and retrieval of personas' private writings."""
    
    def __init__(self, base_path: str = "archives"):
        self.logger = logging.getLogger(__name__)
        self.base_path = Path(base_path)
        
        # Create archive directories for each persona
        self.personas = ["mary_shelley", "lord_byron", "percy_shelley", "herman_melville"]
        self.categories = [
            "letters",
            "diary_entries",
            "private_poems",
            "intimate_thoughts",
            "conversations",
            "unfinished_works"
        ]
        
        self._initialize_directories()
    
    def _initialize_directories(self):
        """Create the necessary directory structure."""
        try:
            # Create base archives directory
            self.base_path.mkdir(exist_ok=True)
            
            # Create directories for each persona
            for persona in self.personas:
                persona_path = self.base_path / persona
                persona_path.mkdir(exist_ok=True)
                
                # Create category subdirectories
                for category in self.categories:
                    category_path = persona_path / category
                    category_path.mkdir(exist_ok=True)
                    
                    # Create an index file for each category
                    index_file = category_path / "index.json"
                    if not index_file.exists():
                        with open(index_file, "w") as f:
                            json.dump({"entries": []}, f, indent=2)
            
            self.logger.info("Archive directories initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize archive directories: {str(e)}")
            raise

    def store_writing(self, 
                     persona: str, 
                     category: str, 
                     content: str, 
                     metadata: Dict[str, Any]) -> str:
        """Store a new piece of writing in the archives."""
        try:
            # Validate inputs
            if persona not in self.personas:
                raise ValueError(f"Invalid persona: {persona}")
            if category not in self.categories:
                raise ValueError(f"Invalid category: {category}")
            
            # Generate timestamp and filename
            timestamp = datetime.now().isoformat()
            filename = f"{timestamp}_{metadata.get('title', 'untitled').lower().replace(' ', '_')}.json"
            
            # Prepare the full entry
            entry = {
                "timestamp": timestamp,
                "content": content,
                "metadata": metadata
            }
            
            # Save the entry
            file_path = self.base_path / persona / category / filename
            with open(file_path, "w") as f:
                json.dump(entry, f, indent=2)
            
            # Update the index
            index_path = self.base_path / persona / category / "index.json"
            with open(index_path, "r") as f:
                index = json.load(f)
            
            index["entries"].append({
                "filename": filename,
                "timestamp": timestamp,
                "title": metadata.get("title", "Untitled"),
                "summary": metadata.get("summary", ""),
                "tags": metadata.get("tags", [])
            })
            
            with open(index_path, "w") as f:
                json.dump(index, f, indent=2)
            
            self.logger.info(f"Stored new writing: {filename} for {persona}")
            return filename
            
        except Exception as e:
            self.logger.error(f"Failed to store writing: {str(e)}")
            raise

    def store_interaction(self, 
                         participants: List[str], 
                         interaction_type: str,
                         content: str,
                         metadata: Dict[str, Any]) -> List[str]:
        """Store an interaction between multiple personas."""
        try:
            # Validate participants
            for participant in participants:
                if participant not in self.personas:
                    raise ValueError(f"Invalid participant: {participant}")
            
            # Generate timestamp and base filename
            timestamp = datetime.now().isoformat()
            base_filename = f"{timestamp}_{interaction_type.lower()}.json"
            
            # Prepare the interaction entry
            entry = {
                "timestamp": timestamp,
                "participants": participants,
                "interaction_type": interaction_type,
                "content": content,
                "metadata": metadata
            }
            
            stored_files = []
            # Store a copy in each participant's conversations directory
            for participant in participants:
                file_path = self.base_path / participant / "conversations" / base_filename
                with open(file_path, "w") as f:
                    json.dump(entry, f, indent=2)
                stored_files.append(str(file_path))
                
                # Update the participant's conversation index
                index_path = self.base_path / participant / "conversations" / "index.json"
                with open(index_path, "r") as f:
                    index = json.load(f)
                
                index["entries"].append({
                    "filename": base_filename,
                    "timestamp": timestamp,
                    "interaction_type": interaction_type,
                    "participants": participants,
                    "summary": metadata.get("summary", "")
                })
                
                with open(index_path, "w") as f:
                    json.dump(index, f, indent=2)
            
            self.logger.info(f"Stored interaction between {', '.join(participants)}")
            return stored_files
            
        except Exception as e:
            self.logger.error(f"Failed to store interaction: {str(e)}")
            raise

    def retrieve_writings(self, 
                         persona: str, 
                         category: str, 
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None,
                         tags: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """Retrieve writings from the archives based on criteria."""
        try:
            if persona not in self.personas:
                raise ValueError(f"Invalid persona: {persona}")
            if category not in self.categories:
                raise ValueError(f"Invalid category: {category}")
            
            # Load the index
            index_path = self.base_path / persona / category / "index.json"
            with open(index_path, "r") as f:
                index = json.load(f)
            
            # Filter entries based on criteria
            filtered_entries = []
            for entry in index["entries"]:
                # Apply date filters if specified
                if start_date and entry["timestamp"] < start_date:
                    continue
                if end_date and entry["timestamp"] > end_date:
                    continue
                    
                # Apply tag filter if specified
                if tags:
                    entry_tags = set(entry.get("tags", []))
                    if not any(tag in entry_tags for tag in tags):
                        continue
                
                # Load the full content
                file_path = self.base_path / persona / category / entry["filename"]
                with open(file_path, "r") as f:
                    full_entry = json.load(f)
                
                filtered_entries.append(full_entry)
            
            return filtered_entries
            
        except Exception as e:
            self.logger.error(f"Failed to retrieve writings: {str(e)}")
            raise

    def get_recent_interactions(self, 
                              persona: str, 
                              limit: int = 10) -> List[Dict[str, Any]]:
        """Get the most recent interactions for a persona."""
        try:
            if persona not in self.personas:
                raise ValueError(f"Invalid persona: {persona}")
            
            # Load the conversation index
            index_path = self.base_path / persona / "conversations" / "index.json"
            with open(index_path, "r") as f:
                index = json.load(f)
            
            # Sort entries by timestamp and take the most recent ones
            sorted_entries = sorted(
                index["entries"], 
                key=lambda x: x["timestamp"], 
                reverse=True
            )[:limit]
            
            # Load the full content for each entry
            recent_interactions = []
            for entry in sorted_entries:
                file_path = self.base_path / persona / "conversations" / entry["filename"]
                with open(file_path, "r") as f:
                    full_entry = json.load(f)
                recent_interactions.append(full_entry)
            
            return recent_interactions
            
        except Exception as e:
            self.logger.error(f"Failed to get recent interactions: {str(e)}")
            raise
