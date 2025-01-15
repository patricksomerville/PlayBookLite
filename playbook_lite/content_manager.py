"""Content manager for handling external text storage"""
import os
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

class ContentManager:
    """Manages external content storage and retrieval"""
    
    def __init__(self, storage_path: str = "content_storage"):
        """Initialize content manager with storage location"""
        self.storage_path = storage_path
        self._ensure_storage_exists()
        
    def _ensure_storage_exists(self) -> None:
        """Create storage directory if it doesn't exist"""
        try:
            if not os.path.exists(self.storage_path):
                os.makedirs(self.storage_path)
                logger.info(f"Created storage directory at {self.storage_path}")
        except Exception as e:
            logger.error(f"Failed to create storage directory: {str(e)}")
            raise

    def store_content(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Store content and return reference ID"""
        try:
            # Generate unique reference ID based on timestamp
            ref_id = f"content_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create content object with metadata
            content_obj = {
                "content": content,
                "metadata": metadata or {},
                "created_at": datetime.now().isoformat(),
            }
            
            # Save to file
            file_path = os.path.join(self.storage_path, f"{ref_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content_obj, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Stored content with reference ID: {ref_id}")
            return ref_id
            
        except Exception as e:
            logger.error(f"Failed to store content: {str(e)}")
            raise

    def get_content(self, ref_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve content by reference ID"""
        try:
            file_path = os.path.join(self.storage_path, f"{ref_id}.json")
            if not os.path.exists(file_path):
                logger.warning(f"Content not found for reference ID: {ref_id}")
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                content_obj = json.load(f)
                
            logger.debug(f"Retrieved content for reference ID: {ref_id}")
            return content_obj
            
        except Exception as e:
            logger.error(f"Failed to retrieve content: {str(e)}")
            return None

    def update_metadata(self, ref_id: str, metadata: Dict[str, Any]) -> bool:
        """Update metadata for existing content"""
        try:
            content_obj = self.get_content(ref_id)
            if not content_obj:
                return False
                
            content_obj["metadata"].update(metadata)
            content_obj["updated_at"] = datetime.now().isoformat()
            
            file_path = os.path.join(self.storage_path, f"{ref_id}.json")
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(content_obj, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Updated metadata for reference ID: {ref_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update metadata: {str(e)}")
            return False
