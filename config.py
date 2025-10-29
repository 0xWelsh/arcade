"""
has game constants, colors, and settings
"""

import os
import pygame


GAME_TITLE = "Cyber Arcade"
VERSION = "1.0.0"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
FULLSCREEN = False

# colors
NEON_BLUE = (0, 195, 255)
NEON_PINK = (255, 0, 128)
NEON_GREEN = (57, 255, 20)
NEON_PURPLE = (180, 0, 255)
NEON_ORANGE = (255, 100, 0)
NEON_YELLOW = (255, 255, 0)

DARK_BLUE = (10, 20, 40)
DARK_PURPLE = (30, 10, 50)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# game colors by the type
COLORS = {
    "tcp": NEON_GREEN,
    "udp": NEON_BLUE,
    "malicious": NEON_PINK,
    "virus": NEON_PINK,
    "trojan": NEON_ORANGE,
    "ransomware": NEON_PURPLE,
    "player": NEON_BLUE,
    "ui": NEON_GREEN,
    "background": DARK_BLUE,
    "text": WHITE,
    "warning": NEON_ORANGE
}

# paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "assets")
IMAGES_PATH = os.path.join(ASSETS_PATH, "images")
AUDIO_PATH = os.path.join(ASSETS_PATH, "audio")
FONTS_PATH = os.path.join(ASSETS_PATH, "fonts")
DATA_PATH = os.path.join(BASE_DIR, "data")

# game settings
DEFAULT_PLAYER_SPEED = 5
DEFAULT_GAME_TIME = 60 # this is seconds

# input settings
KEY_REPEAT_DELAY = 200 # ms
KEY_REPEAT_INTERVAL = 50 # ms

# audio settings
MASTER_VOLUME = 0.7
MUSIC_VOLUME = 0.5
SFX_VOLUME = 0.8

# game states
STATE_MAIN_MENU = "main_menu"
STATE_ARCADE_HUB = "arcade_hub"
STATE_GAME_SELECT = "game_select"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_OPTIONS = "options"

# available games
GAMES = {
    "packet_runner": "Packet Runner",
    "firewall_defender": "Firewall Defender",
    "code_breaker": "Code Breaker",
    "social_engineering": "Social Engineering Sim",
    "ctf_racer": "CTF Racer"
}

# achievements
ACHIEVEMENTS = {
    "first_blood": {"name": "First Blood", "description": "Catch your first packet", "points": 10},
    "firewall_master": {"name": "Firewall Master", "description": "Complete Firewall Defender without leaks", "points": 50},
    "code_cracker": {"name": "Code Cracker", "description": "Solve 10 cryptography puzzles", "points": 30},
    "social_engineer": {"name": "Social Engineer", "description": "Detect 20 phishing attempts", "points": 40},
    "speed_demon": {"name": "Speed Demon", "description": "Win CTF Racer in under 2 minutes", "points": 25},
    "perfect_game": {"name": "Perfect Game", "description": "Get maximum score in all mini-games", "points": 100}
}