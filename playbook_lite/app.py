"""Flask app for PlayBook's web interface"""

from flask import Flask, render_template, jsonify, request
from .game_interface import TextInterface
from .ascii_art import get_art
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
game = None

@app.route('/')
def index():
    """Serve the DOS terminal interface"""
    logger.debug("Serving index page")
    return render_template('dos_terminal.html')

@app.route('/start')
def start_game():
    """Initialize and start a new game"""
    global game
    logger.debug("Starting new game")
    game = TextInterface()
    
    # Get both the title screen and character selection screen
    title_screen = get_art('title')
    char_select = game.get_character_select_screen()
    
    logger.debug(f"Got title screen: {bool(title_screen)}")
    return jsonify({
        'title_screen': title_screen,
        'text': char_select  # Send character selection text to display
    })

@app.route('/command', methods=['POST'])
def handle_command():
    """Process game commands"""
    command = request.json.get('command', '').strip().upper()
    logger.debug(f"Handling command: {command}")
    
    # Get response from game engine
    response = game.handle_command(command)
    logger.debug(f"Got response: {response}")
    
    return jsonify({
        'text': response.get('text', ''),
        'ascii_art': response.get('ascii_art', None)
    })

def run_server():
    """Run the Flask development server"""
    logger.info("Starting Flask server")
    app.run(debug=True, port=5003)