"""
CyberPunk Arcade - Main Game Engine
Handles the game loop, scene management, and core functionality
"""

import pygame
import sys
import os
from config import *

class CyberpunkArcade:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.mixer.init()
        
        # Create display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"{GAME_TITLE} v{VERSION}")
        
        # Game clock
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.current_state = STATE_MAIN_MENU
        self.previous_state = None
        self.game_instance = None
        
        # Game data
        self.score = 0
        self.high_score = 0
        self.unlocked_games = ["packet_runner", "firewall_defender", "code_breaker", "social_engineering", "ctf_racer"]
        self.achievements = {}
        
        # Input
        self.keys_pressed = set()
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        
        # Load game data
        self._load_game_data()
        
    def _load_game_data(self):
        """Load saved game data"""
        try:
            # Placeholder - will implement proper save system
            self.high_score = 0
            print("Game data loaded successfully")
        except Exception as e:
            print(f"Error loading game data: {e}")
            
    def _save_game_data(self):
        """Save game data"""
        try:
            # Placeholder - will implement proper save system
            print("Game data saved successfully")
        except Exception as e:
            print(f"Error saving game data: {e}")
    
    def run(self):
        """Main game loop"""
        print("Starting CyberPunk Arcade...")
        
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(FPS)
            
        self.quit_game()
    
    def handle_events(self):
        """Handle all pygame events"""
        self.mouse_clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)
                
                # Global key bindings
                if event.key == pygame.K_ESCAPE:
                    self.handle_escape()
                elif event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                    
            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed.remove(event.key)
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.mouse_clicked = True
                    
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                
        # Update key state for continuous presses
        self.keys_pressed = set(pygame.key.get_pressed())
    
    def handle_escape(self):
        """Handle ESC key press based on current state"""
        if self.current_state == STATE_MAIN_MENU:
            self.running = False
        elif self.current_state in [STATE_ARCADE_HUB, STATE_GAME_SELECT]:
            self.current_state = STATE_MAIN_MENU
        elif self.current_state == STATE_PAUSED:
            self.current_state = self.previous_state
        else:
            self.previous_state = self.current_state
            self.current_state = STATE_PAUSED
    
    def toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode"""
        global FULLSCREEN
        FULLSCREEN = not FULLSCREEN
        
        if FULLSCREEN:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    def update(self):
        """Update game state based on current scene"""
        if self.current_state == STATE_MAIN_MENU:
            self.update_main_menu()
        elif self.current_state == STATE_ARCADE_HUB:
            self.update_arcade_hub()
        elif self.current_state == STATE_GAME_SELECT:
            self.update_game_select()
        elif self.current_state == STATE_PAUSED:
            self.update_pause_menu()
        elif self.current_state == STATE_GAME_OVER:
            self.update_game_over()
        elif self.current_state == STATE_OPTIONS:
            self.update_options_menu()
        elif self.current_state in GAMES:
            self.update_game()
            
        # Update current game instance if active
        if self.game_instance and hasattr(self.game_instance, 'update'):
            self.game_instance.update()
    
    def update_main_menu(self):
        """Update main menu state"""
        # Check for number keys (both numpad and number row)
        keys = pygame.key.get_pressed()
        
        # Number row keys (1, 2, 3, 4, 5)
        if keys[pygame.K_1] and "packet_runner" in self.unlocked_games:
            self.start_game("packet_runner")
        elif keys[pygame.K_2] and "firewall_defender" in self.unlocked_games:
            self.start_game("firewall_defender")
        elif keys[pygame.K_3] and "code_breaker" in self.unlocked_games:
            self.start_game("code_breaker")
        elif keys[pygame.K_4] and "social_engineering" in self.unlocked_games:
            self.start_game("social_engineering")
        elif keys[pygame.K_5] and "ctf_racer" in self.unlocked_games:
            self.start_game("ctf_racer")
        elif keys[pygame.K_o]:
            self.current_state = STATE_OPTIONS
    
    def update_arcade_hub(self):
        """Update arcade hub state"""
        pass
    
    def update_game_select(self):
        """Update game selection screen"""
        pass
    
    def update_pause_menu(self):
        """Update pause menu"""
        pass
    
    def update_game_over(self):
        """Update game over screen"""
        pass
    
    def update_options_menu(self):
        """Update options menu"""
        if pygame.K_ESCAPE in self.keys_pressed:
            self.current_state = STATE_MAIN_MENU
    
    def update_game(self):
        """Update current mini-game"""
        pass
    
    def start_game(self, game_name):
        """Start a specific mini-game"""
        try:
            print(f"Starting game: {game_name}")
            
            # Import and initialize the game
            if game_name == "packet_runner":
                from games.packet_runner.packet_runner import PacketRunner
                self.game_instance = PacketRunner(self)
            elif game_name == "firewall_defender":
                from games.firewall_defender.firewall_defender import FirewallDefender
                self.game_instance = FirewallDefender(self)
            elif game_name == "code_breaker":
                from games.code_breaker.code_breaker import CodeBreaker
                self.game_instance = CodeBreaker(self)
            elif game_name == "social_engineering":
                from games.social_engineering.social_engineering import SocialEngineering
                self.game_instance = SocialEngineering(self)
            elif game_name == "ctf_racer":
                from games.ctf_racer.ctf_racer import CTFRacer
                self.game_instance = CTFRacer(self)
            
            self.current_state = game_name
            
        except ImportError as e:
            print(f"Error loading game {game_name}: {e}")
            print("Game not implemented yet!")
        except Exception as e:
            print(f"Error starting game {game_name}: {e}")
    
    def render(self):
        """Render the current game state"""
        # Clear screen with background color
        self.screen.fill(BLACK)
        
        # Render based on current state
        if self.current_state == STATE_MAIN_MENU:
            self.render_main_menu()
        elif self.current_state == STATE_ARCADE_HUB:
            self.render_arcade_hub()
        elif self.current_state in GAMES:
            self.render_game()
        elif self.current_state == STATE_PAUSED:
            self.render_pause_menu()
        elif self.current_state == STATE_GAME_OVER:
            self.render_game_over()
        elif self.current_state == STATE_OPTIONS:
            self.render_options_menu()
        
        # Update display
        pygame.display.flip()
    
    def render_main_menu(self):
        """Render the main menu"""
        # Title
        title_font = pygame.font.Font(None, 74)
        title_text = title_font.render(GAME_TITLE, True, NEON_BLUE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.Font(None, 36)
        subtitle_text = subtitle_font.render("Cybersecurity Mini-Games Collection", True, NEON_GREEN)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 160))
        self.screen.blit(subtitle_text, subtitle_rect)
        
        # Game options
        option_font = pygame.font.Font(None, 32)
        options = []
        
        for i, (game_id, game_name) in enumerate(GAMES.items()):
            if game_id in self.unlocked_games:
                color = NEON_GREEN
                text = f"{i+1}. {game_name}"
            else:
                color = GRAY
                text = f"{i+1}. ??? (Locked)"
            options.append((text, color))
        
        # Add other menu options
        options.append(("O. Options", NEON_BLUE))
        options.append(("ESC. Exit", NEON_PINK))
        
        # Render options
        for i, (text, color) in enumerate(options):
            option_text = option_font.render(text, True, color)
            option_rect = option_text.get_rect(center=(SCREEN_WIDTH//2, 250 + i*50))
            self.screen.blit(option_text, option_rect)
        
        # Footer
        footer_font = pygame.font.Font(None, 24)
        footer_text = footer_font.render(f"Version {VERSION} | Press number keys to select games", True, LIGHT_GRAY)
        footer_rect = footer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
        self.screen.blit(footer_text, footer_rect)
    
    def render_arcade_hub(self):
        """Render arcade hub"""
        pass
    
    def render_game(self):
        """Render the current mini-game"""
        if self.game_instance and hasattr(self.game_instance, 'render'):
            self.game_instance.render()
        else:
            # Fallback rendering if game doesn't implement render
            font = pygame.font.Font(None, 48)
            text = font.render(f"Playing: {GAMES.get(self.current_state, self.current_state)}", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(text, text_rect)
            
            hint_font = pygame.font.Font(None, 24)
            hint_text = hint_font.render("Game rendering not implemented yet", True, GRAY)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(hint_text, hint_rect)
    
    def render_pause_menu(self):
        """Render pause menu overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        font = pygame.font.Font(None, 72)
        text = font.render("PAUSED", True, NEON_BLUE)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        self.screen.blit(text, text_rect)
        
        # Instructions
        instruction_font = pygame.font.Font(None, 32)
        instruction = instruction_font.render("Press ESC to resume", True, WHITE)
        instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(instruction, instruction_rect)
    
    def render_game_over(self):
        """Render game over screen"""
        pass
    
    def render_options_menu(self):
        """Render options menu"""
        self.screen.fill(DARK_BLUE)
        
        # Title
        font = pygame.font.Font(None, 64)
        title = font.render("OPTIONS", True, NEON_BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.screen.blit(title, title_rect)
        
        # Options placeholder
        option_font = pygame.font.Font(None, 32)
        options = [
            "Audio Settings",
            "Video Settings", 
            "Controls",
            "Back to Main Menu (ESC)"
        ]
        
        for i, option in enumerate(options):
            text = option_font.render(option, True, NEON_GREEN)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, 200 + i*60))
            self.screen.blit(text, text_rect)
    
    def quit_game(self):
        """Cleanup and quit the game"""
        print("Shutting down game...")
        self._save_game_data()
        pygame.quit()
        sys.exit()
    
    def add_score(self, points):
        """Add points to total score"""
        self.score += points
        if self.score > self.high_score:
            self.high_score = self.score
    
    def unlock_achievement(self, achievement_id):
        """Unlock an achievement"""
        if achievement_id in ACHIEVEMENTS and achievement_id not in self.achievements:
            self.achievements[achievement_id] = True
            achievement = ACHIEVEMENTS[achievement_id]
            print(f"Achievement Unlocked: {achievement['name']} - {achievement['description']}")
            return True
        return False
    
    def unlock_game(self, game_id):
        """Unlock a new game"""
        if game_id in GAMES and game_id not in self.unlocked_games:
            self.unlocked_games.append(game_id)
            print(f"Game Unlocked: {GAMES[game_id]}")
            return True
        return False