"""DOS-style window interface using curses"""

import curses
import time
from typing import Optional, Tuple
from dataclasses import dataclass

@dataclass
class WindowDimensions:
    height: int = 25  # Classic DOS terminal height
    width: int = 80   # Classic DOS terminal width
    start_y: int = 0
    start_x: int = 0

class DOSWindow:
    def __init__(self):
        self.screen = None
        self.main_window = None
        self.dimensions = WindowDimensions()
        
    def __enter__(self):
        """Initialize curses screen"""
        self.screen = curses.initscr()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Classic DOS colors
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        self.main_window = self._create_main_window()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup curses"""
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()
        
    def _create_main_window(self) -> "curses.window":
        """Create main DOS-style window"""
        h, w = self.screen.getmaxyx()
        window = curses.newwin(
            self.dimensions.height,
            self.dimensions.width,
            (h - self.dimensions.height) // 2,
            (w - self.dimensions.width) // 2
        )
        window.bkgd(' ', curses.color_pair(1))
        window.box()
        window.refresh()
        return window
        
    def write_text(self, y: int, x: int, text: str, refresh: bool = True):
        """Write text at specific coordinates"""
        try:
            self.main_window.addstr(y, x, text[:self.dimensions.width-2])
            if refresh:
                self.main_window.refresh()
        except curses.error:
            pass  # Ignore errors from writing at invalid positions
            
    def clear_window(self):
        """Clear the window content"""
        self.main_window.clear()
        self.main_window.box()
        self.main_window.refresh()
        
    def get_input(self, prompt: str = "> ") -> str:
        """Get user input with prompt"""
        curses.echo()  # Show typed characters
        self.main_window.move(self.dimensions.height-2, 0)
        self.write_text(self.dimensions.height-2, 0, prompt)
        
        # Create input buffer
        input_y = self.dimensions.height-2
        input_x = len(prompt)
        self.main_window.move(input_y, input_x)
        
        # Get input
        input_str = ""
        while True:
            try:
                char = self.main_window.get_wch()
                if isinstance(char, str) and ord(char) == 10:  # Enter key
                    break
                elif isinstance(char, str):
                    input_str += char
                    self.write_text(input_y, input_x, input_str)
            except curses.error:
                continue
                
        curses.noecho()
        return input_str.strip()
        
    def render_ascii_art(self, art: str, with_effects: bool = True):
        """Render ASCII art with optional loading effects"""
        if with_effects:
            # Show static effect
            for _ in range(3):
                self.clear_window()
                for y in range(1, self.dimensions.height-1):
                    noise = ''.join(' .,:;=+*#@'[ord(c) % 10] for c in art[y*10:(y+1)*10])
                    self.write_text(y, 1, noise)
                time.sleep(0.2)
                
        # Render actual art
        lines = art.split('\n')
        start_y = (self.dimensions.height - len(lines)) // 2
        
        for i, line in enumerate(lines):
            if with_effects:
                time.sleep(0.1)  # Slow reveal
            self.write_text(start_y + i, 1, line)
            
    def show_title_screen(self):
        """Display the title screen"""
        title = [
            "╔════════════════════════════════════════╗",
            "║             P L A Y B O O K            ║",
            "║                                        ║",
            "║          M O B Y   D I C K            ║",
            "║        An Interactive Journey          ║",
            "║                                        ║",
            "║    Based on the novel by H. Melville   ║",
            "╚════════════════════════════════════════╝"
        ]
        
        start_y = (self.dimensions.height - len(title)) // 2
        for i, line in enumerate(title):
            self.write_text(start_y + i, (self.dimensions.width - len(line)) // 2, line)
            time.sleep(0.1)  # Dramatic reveal
