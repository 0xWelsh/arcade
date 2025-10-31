# games/packet_runner/packet_runner.py
import pygame
import random
from games.base_game import BaseGame
from config import *

class PacketRunner(BaseGame):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.game_time = 60.0  # 60 seconds game
        self.time_left = self.game_time
        self.game_active = True  # ← ADD THIS LINE
        
        # Player
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT - 100
        self.player_speed = 8
        self.player_width = 80
        self.player_height = 20
        
        # Packets
        self.packets = []
        self.spawn_timer = 0
        self.spawn_interval = 0.8  # seconds between spawns
        
        print("Packet Runner started! Catch TCP (green) and UDP (blue) packets. Avoid malicious (red) packets!")
        
    def update(self):
        if not self.game_active:
            return
            
        # Update timer
        self.time_left -= 1/60  # Assuming 60 FPS
        if self.time_left <= 0:
            self.end_game()
            
        self.handle_input()
        self.update_packets()
        self.spawn_packets()
        self.check_collisions()
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x < SCREEN_WIDTH - self.player_width:
            self.player_x += self.player_speed
            
    def spawn_packets(self):
        self.spawn_timer += 1/60
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            
            # Random packet type with weights
            packet_type = random.choices(
                ["tcp", "udp", "malicious"],
                weights=[5, 3, 2]  # TCP most common, malicious least common
            )[0]
            
            self.packets.append({
                "x": random.randint(50, SCREEN_WIDTH - 50),
                "y": -30,
                "type": packet_type,
                "speed": random.uniform(3, 6)
            })
            
    def update_packets(self):
        for packet in self.packets[:]:
            packet["y"] += packet["speed"]
            # Remove packets that go off screen
            if packet["y"] > SCREEN_HEIGHT:
                self.packets.remove(packet)
                
    def check_collisions(self):
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_width, self.player_height)
        
        for packet in self.packets[:]:
            packet_rect = pygame.Rect(packet["x"] - 15, packet["y"] - 15, 30, 30)
            
            if player_rect.colliderect(packet_rect):
                self.handle_packet_catch(packet["type"])
                self.packets.remove(packet)
                
    def handle_packet_catch(self, packet_type):
        if packet_type == "tcp":
            self.score += 10
            print(f"✅ Caught TCP packet! +10 points (Total: {self.score})")
        elif packet_type == "udp":
            self.score += 5
            print(f"✅ Caught UDP packet! +5 points (Total: {self.score})")
        elif packet_type == "malicious":
            self.score -= 15
            print(f"❌ Caught malicious packet! -15 points (Total: {self.score})")
            
        # Update global score
        self.game_engine.add_score(self.score)
        
    def render(self):
        # Draw player (simple rectangle for now)
        pygame.draw.rect(self.screen, NEON_BLUE, 
                        (self.player_x, self.player_y, self.player_width, self.player_height))
        
        # Draw packets
        for packet in self.packets:
            color = NEON_GREEN if packet["type"] == "tcp" else \
                   NEON_BLUE if packet["type"] == "udp" else \
                   NEON_PINK
            pygame.draw.circle(self.screen, color, (int(packet["x"]), int(packet["y"])), 15)
        
        # Draw UI
        self.render_ui()
        
    def render_ui(self):
        font = pygame.font.Font(None, 36)
        
        # Score
        score_text = font.render(f"Score: {self.score}", True, NEON_GREEN)
        self.screen.blit(score_text, (20, 20))
        
        # Timer
        time_text = font.render(f"Time: {int(self.time_left)}", True, NEON_BLUE)
        self.screen.blit(time_text, (SCREEN_WIDTH - 150, 20))
        
        # Instructions
        small_font = pygame.font.Font(None, 24)
        instructions = [
            "← → : Move",
            "TCP (Green): +10",
            "UDP (Blue): +5", 
            "Malicious (Red): -15"
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, LIGHT_GRAY)
            self.screen.blit(text, (20, 60 + i*25))