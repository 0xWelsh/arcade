# games/code_breaker/code_breaker.py
import pygame
import random
import string
from games.base_game import BaseGame
from config import *

class CodeBreaker(BaseGame):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.game_active = True
        self.current_level = 1
        self.max_levels = 5
        self.current_puzzle = None
        
        self.initialize_puzzle()
        print("Code Breaker started! Crack the codes before time runs out!")
        
    def initialize_puzzle(self):
        if self.current_level == 1:
            self.current_puzzle = self.create_caesar_cipher()
        elif self.current_level == 2:
            self.current_puzzle = self.create_substitution_cipher()
        elif self.current_level == 3:
            self.current_puzzle = self.create_reverse_cipher()
        elif self.current_level == 4:
            self.current_puzzle = self.create_binary_cipher()
        else:
            self.current_puzzle = self.create_mixed_cipher()
            
    def create_caesar_cipher(self):
        # Caesar cipher - shift letters
        plaintext = "THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG"
        shift = random.randint(1, 25)
        ciphertext = ""
        
        for char in plaintext:
            if char.isalpha():
                shifted = chr((ord(char) - 65 + shift) % 26 + 65)
                ciphertext += shifted
            else:
                ciphertext += char
                
        return {
            'type': 'caesar',
            'ciphertext': ciphertext,
            'plaintext': plaintext,
            'shift': shift,
            'hint': f"Letters are shifted by a fixed number",
            'time_limit': 120
        }
        
    def create_substitution_cipher(self):
        # Simple substitution cipher
        alphabet = list(string.ascii_uppercase)
        shuffled = alphabet.copy()
        random.shuffle(shuffled)
        
        plaintext = "CRYPTOGRAPHY IS FUN"
        ciphertext = ""
        
        for char in plaintext:
            if char.isalpha():
                index = alphabet.index(char)
                ciphertext += shuffled[index]
            else:
                ciphertext += char
                
        return {
            'type': 'substitution',
            'ciphertext': ciphertext,
            'plaintext': plaintext,
            'mapping': dict(zip(alphabet, shuffled)),
            'hint': "Each letter is consistently replaced with another",
            'time_limit': 180
        }
        
    def create_reverse_cipher(self):
        # Reverse the text
        plaintext = "REVERSE THIS MESSAGE"
        ciphertext = plaintext[::-1]
        
        return {
            'type': 'reverse',
            'ciphertext': ciphertext,
            'plaintext': plaintext,
            'hint': "The text is reversed",
            'time_limit': 60
        }
        
    def create_binary_cipher(self):
        # Convert to binary
        plaintext = "BINARY"
        ciphertext = ' '.join(format(ord(c), '08b') for c in plaintext)
        
        return {
            'type': 'binary',
            'ciphertext': ciphertext,
            'plaintext': plaintext,
            'hint': "Convert binary to ASCII characters",
            'time_limit': 150
        }
        
    def create_mixed_cipher(self):
        # Mixed challenge
        plaintext = "FINAL CHALLENGE"
        # Reverse then Caesar shift
        reversed_text = plaintext[::-1]
        shift = 13
        ciphertext = ""
        
        for char in reversed_text:
            if char.isalpha():
                shifted = chr((ord(char) - 65 + shift) % 26 + 65)
                ciphertext += shifted
            else:
                ciphertext += char
                
        return {
            'type': 'mixed',
            'ciphertext': ciphertext,
            'plaintext': plaintext,
            'hint': "Combination of multiple techniques",
            'time_limit': 200
        }
        
    def update(self):
        if not self.game_active:
            return
            
        self.handle_input()
        
    def handle_input(self):
        # For now, we'll handle input in render. In full version, add text input.
        pass
        
    def check_solution(self, user_input):
        if user_input.upper() == self.current_puzzle['plaintext']:
            self.score += 100 * self.current_level
            self.current_level += 1
            
            if self.current_level > self.max_levels:
                print("🎉 All levels completed! You're a master cryptographer!")
                self.end_game()
            else:
                print(f"✅ Level {self.current_level-1} completed! Starting level {self.current_level}")
                self.initialize_puzzle()
            return True
        return False
        
    def render(self):
        if not self.current_puzzle:
            return
            
        # Display puzzle
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 36)
        font_small = pygame.font.Font(None, 24)
        
        # Title
        title = font_large.render(f"Code Breaker - Level {self.current_level}", True, NEON_BLUE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Ciphertext
        cipher_text = font_medium.render("Ciphertext:", True, NEON_GREEN)
        self.screen.blit(cipher_text, (50, 120))
        
        cipher_display = font_medium.render(self.current_puzzle['ciphertext'], True, WHITE)
        self.screen.blit(cipher_display, (50, 160))
        
        # Hint
        hint_text = font_small.render(f"Hint: {self.current_puzzle['hint']}", True, NEON_PURPLE)
        self.screen.blit(hint_text, (50, 220))
        
        # Instructions
        instructions = [
            "Type your answer (not implemented in demo)",
            f"Level {self.current_level}/{self.max_levels}",
            f"Score: {self.score}",
            "Press ESC to return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font_small.render(instruction, True, LIGHT_GRAY)
            self.screen.blit(text, (50, 280 + i*30))
            
        # For demo purposes, show the answer
        if self.current_level <= 3:  # Only show for first few levels as hint
            answer_text = font_small.render(f"Answer: {self.current_puzzle['plaintext']}", True, NEON_ORANGE)
            self.screen.blit(answer_text, (SCREEN_WIDTH - 300, SCREEN_HEIGHT - 50))