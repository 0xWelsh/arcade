import pygame
from config import *

class BaseGame:
    def __init__(self,game_engine):
        self.game_engine = game_engine
        self.screen = game_engine.screen
        self.running = True
        self.score = 0


    def update(self):
        """Update game logic - to be implemented by child classes"""
        pass

    def render(self):
        """Render game - to be implemented by child classes"""
        pass

    def handle_input(self):
        """Handle input - to be implemented by child classes"""
        pass

    def end_game(self):
        """End the current game"""
        self.running = False
        self.game_engine.current_state = "main_menu"