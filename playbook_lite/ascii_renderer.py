"""ASCII art renderer with dramatic reveal and sound effects"""

import time
import random
import sys
import os
from typing import List

class ASCIIRenderer:
    """Renders ASCII art with dramatic effects"""
    
    @staticmethod
    def render_art(art: str, render_speed: float = 0.001):
        """Render ASCII art line by line with 'loading' effect"""
        # First, create static effect
        ASCIIRenderer._static_effect()
        
        # Play loading sound
        ASCIIRenderer._play_sound("loading")
        
        # Convert art to lines
        lines = art.split('\n')
        
        # Calculate dimensions
        max_width = max(len(line) for line in lines)
        height = len(lines)
        
        # Create "scanning" effect
        for y in range(height):
            # Print static for current line
            sys.stdout.write('\r' + ''.join(random.choice(' .,:;=+*#@') for _ in range(max_width)))
            sys.stdout.flush()
            time.sleep(render_speed)
            
            # Replace with actual art line
            sys.stdout.write('\r' + lines[y])
            sys.stdout.flush()
            time.sleep(render_speed)
            print()  # Move to next line
            
        # Play completion sound
        ASCIIRenderer._play_sound("complete")
        
        # Let the art linger
        time.sleep(1)
    
    @staticmethod
    def _static_effect(duration: float = 0.5, lines: int = 5):
        """Create brief static effect"""
        for _ in range(lines):
            # Print random static
            sys.stdout.write('\r' + ''.join(random.choice(' .,:;=+*#@') for _ in range(80)))
            sys.stdout.flush()
            time.sleep(duration/lines)
            print()
    
    @staticmethod
    def _play_sound(sound_type: str):
        """Play appropriate sound effect using system beep"""
        if sound_type == "loading":
            # Three ascending beeps
            for freq in [440, 540, 640]:
                sys.stdout.write('\a')  # ASCII bell
                sys.stdout.flush()
                time.sleep(0.1)
        elif sound_type == "complete":
            # One final deeper beep
            sys.stdout.write('\a')
            sys.stdout.flush()
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
