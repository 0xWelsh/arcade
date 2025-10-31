"""
handles the game loop, scene management, and the core functionality
"""

import pygame
import sys
import os
from config import *

class CyberpunkArcade:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(f"{GAME_TITLE} v{VERSION}")

        # game clock
        self.clock = pygame.time.Clock()
        self.running = True

        # game state
        self.current_state = STATE_MAIN_MENU
        self.previous_state = None
        self.game_instance = None

        # game data
        self.score = 0
        self.high_score = 0
        self.unlocked_games = ["packet_runner"]
        self.achievements = {}

        self.asset_manager = None
        self.audio_manager = None
        self.save_manager = None

        # input
        self.keys_pressed = set()
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False

        # initialize systems
        self._initialize_managers()
        self._load_game_data()

    def initialize(self):
        """initialize various game managemnt systems"""
        print("Initializing game managers...")

    def _load_game_data(self):
        """load saved game data"""
        try:
            # placeholder, to implement proper save system
            self.high_score = 0
            print("Game data loaded successfully")
        except Exception as e:
            print(f"Error loading game data: {e}")


    def _save_game_data(self):
        """Save game data"""
        try:
            print("Game data saved successfully")
        except Exception as e:
            print(f"Error saving game data: {e}")

    def run(self):
        """main game loop"""
        print(f"Starting {GAME_TITLE}...")


        while self.running:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(FPS)

        self._quit()

    def _handle_events(self):
        """handle all pygame events"""
        self.mouse_clicked = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.keys_pressed.add(event.key)

                if event.key == pygame.K_ESCAPE:
                    self._handle_escape()
                elif event.key == pygame.K_F11:
                    self._toggle_fullscreen()

            elif event.type == pygame.KEYUP:
                if event.key in self.keys_pressed:
                    self.keys_pressed.remove(event.key)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left click
                    self.mouse_clicked = True

            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

        def _handle_escape(self):
            """handle ESC key press on current state"""
            if self.current_state == STATE_MAIN_MENU:
                self.running = False
            elif self.current_state in [STATE_ARCADE_HUB, STATE_GAME_SELECT]:
                self.current_state = STATE_MAIN_MENU
            elif self.current_state == STATE_PAUSED:
                self.current_state = self.previous_state
            else:
                self.previous_state = self.current_state
                self.current_state = STATE_PAUSED

        def _toggle_fullscreen(self):
            """toggle between fullscreen and windowed mode"""
            global FULLSCREEN
            FULLSCREEN = not FULLSCREEN

            if FULLSCREEN:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        def _update(self):
            """update game state based on current scene"""
            if self.current_state == STATE_MAIN_MENU:
                self._update_main_menu()
            elif self.current_state == STATE_ARCADE_HUB:
                self._update_arcade_hub()
            elif self.current_state == STATE_GAME_SELECT:
                self._update_game_select()
            elif self.current_state == STATE_PAUSED:
                self._update_pause_menu()
            elif self.current_state == STATE_GAME_OVER:
                self._update_game_over()
            elif self.current_state == STATE_OPTIONS:
                self._update_options_menu()

            # update current game instance if active
            if self.game_instance and hasattr(self.game_instance, 'update'):
                self.game_instance.update()

        def _update_main_menu(self):
            """update main menu state"""
            # number keys to select a game
            if pygame.K_1 in self.keys_pressed and "packet_runner" in self.unlocked_games:
                self._start_game("packet_runner")
            elif pygame.K_2 in self.keys_pressed and "firewall_defender" in self.unlocked_games:
                self._start_game("firewall_defender")
            elif pygame.K_3 in self.keys_pressed and "code_breaker" in self.unlocked_games:
                self._start_game("code_breaker")
            elif pygame.K_4 in self.keys_pressed and "social_engineering" in self.unlocked_games:
                self._start_game("social_engineering")
            elif pygame.K_5 in self.keys_pressed and "ctf_racer" in self.unlocked_games:
                self._start_game("ctf_racer")
            elif pygame.K_o in self.keys_pressed:
                self.current_state = STATE_OPTIONS

        def _update_arcade_hub(self):
            """update arcade hub state"""
            pass # will be back to this

        def _update_game_select(self):
            """update game selection screen"""
            pass

        def _update_game_menu(self):
            """update pause menu"""
            pass

        def _update_game_over(self):
            """update game over screen"""
            pass

        def _update_options_menu(self):
            """update options menu"""
            if pygame.K_ESCAPE in self.keys_pressed:
                self.current_state = STATE_MAIN_MENU

        def _start_game(self, game_name):
            """start a specific mini_game"""
            try:
                print(f"Starting game: {game_name}")

                # import and initialize the game
                if game_name == "packet_runner":
                    from games.packet_runner.packet_runner import PacketRunner
                    self.game_instance = PacketRunner(self)
                # we will add games here as they are implemented

                self.current_state = game_name

            except ImportError as e:
                print(f"Error loading game {game_name}: {e}")
                print("Game not implemented yet!")
            except Exception as e:
                print(f"Error starting game {game_name}: {e}")

        def _render(self):
            """render the current game state"""
            # clear the screen with background color
            self.screen.fill(BLACK)

            # render based on the curren state
            if self.current_state ==STATE_MAIN_MENU:
                self._render_main_menu()
            elif self.current_state == STATE_ARCADE_HUB:
                self._render_arcade_hub()
            elif self.current_state == GAMES:
                self._render_game()
            elif self.current_state == STATE_PAUSED:
                self._render_pause_menu()
            elif self_current_state == STATE_GAME_OVER:
                self._render_game_over()
            elif self.current_state == STATE_OPTIONS:
                self._render_options_menu()

            # update the display
            pygame.display.flip()

        def _render_main_menu(self):
            """render the main menu"""
            # title
            title_font = pygame.font.Font(None, 74)
            title_text = title_font.render(GAME_TITLE, True, NEON_BLUE)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title_text, title_rect)


            # subtitle
            subtitle_font = pygame.font.Font(None, 36)
            subtitle_text = subtitle_font.render("Cybersecurity Mini_Games Collection", True, NEON_GREEN)
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 160))
            self.screen.blit(subtitle_text, subtitle_rect)

            # game options
            option_font = pygame.font_Font(None, 32)
            options = []

            for i, (game_id, game_name) in enumerate(GAMES.items()):
                if game_id in self.unlocked_games:
                    color = NEON_GREEN
                    text = f"(i+1). {game_name}"
                else:
                    color = GRAY
                    text = f"{i+1}. ??? (Locked)"
                options.append((text, color))

            # more menu options
            options.append(("O, Options", NEON_BLUE))
            options.append(("ESC, Quit", NEON_PINK))

            # render options
            for i, (text, color) in enumerate(options):
                option_text = option_font.render(text, True, color)
                option_rect = option_text.get_rect(center=(SCREEN_WIDTH//2, 250 + i*50))
                self.screen.blit(option_text, option_rect)

            # footer
            footer_font = pygame.font.Font(None, 24)
            footer_text = footer_font.render(f"Version {VERSION} | Press number keys to select games", True, LIGHT_GRAY)
            footer_rect = footer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 30))
            self.screen.blit(footer_text, footer_rect)

        def _render_arcade_hub(self):
            """render arcade hub"""
            pass

        def _render_game(self):
            """render the current mini-game"""
            if self.game_instance and hasattr(self.game_instance, 'render'):
                self.game_instance.render()
            else:
                # fallback rendering if game does not implement render
                font = pygame.font.Font(None, 48)
                text = font.render(f"Playing: {GAMES.get(self.currnet_state, self.current_state)}", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(text, text_rect)

                hint_font = pygame.font.Font(None, 24)
                hint_text = hint_font.render("Game rendering not implemented yet", True, GRAY)
                hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
                self.screen.blit(hint_text, hint_rect)

        def _render_pause_menu(self):
            """render pause menu overlay"""
            # semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            # pause text
            font = pygame.font.Font(None, 72)
            text = font.render("PAUSED", True, NEON_BLUE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(text, text_rect)

            # instructions
            instruction_font = pygame.font.Font(None, 32)
            instruction = instruction_font.render("Press ERC to resume", True, WHITE)
            instruction_rect = instruction.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(instruction, instruction_rect)

        def _render_game_over(self):
            """render game over screen"""
            pass

        def _render_options_menu(self):
            """render options menu"""
            self.screen.fill(DARK_BLUE)

            # title
            font = pygame.font.Font(None, 64)
            title = font.render("OPTIONS", True, NEON_BLUE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(title, title_rect)


            # options placeholder
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

        def _quit(self):
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
            """unlock an achievement"""
            if achievement_id in ACHIEVEMENTS and achievement_id not in self.achievements:
                self.achievements[achievement_id] = True
                achievement = ACHIEVEMENTS[achievement_id]
                print(f"Achievement Unlocked: {achievement['name']} - {achievement['description']}")
                return True
            return False

        def unlock_game(self, game_id):
            """unlock a new game"""
            if game_id in GAMES and game_id not in self.unlocked_games:
                self.unlocked_games.append(game_id)
                print(f"Game Unlocked: {GAMES[game_id]}")
                return True
            return False