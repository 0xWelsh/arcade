# games/firewall_defender/firewall_defender.py
import pygame
import random
import math
from games.base_game import BaseGame
from config import *

class FirewallDefender(BaseGame):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.game_active = True
        self.lives = 10
        self.money = 100
        
        # Game grid
        self.grid_size = 40
        self.grid_width = SCREEN_WIDTH // self.grid_size
        self.grid_height = SCREEN_HEIGHT // self.grid_size
        
        # Towers and enemies
        self.towers = []
        self.enemies = []
        self.projectiles = []
        
        # Waves
        self.current_wave = 1
        self.wave_timer = 0
        self.enemies_per_wave = 5
        
        # Path for enemies (simple left-to-right)
        self.path = [(0, i) for i in range(5, self.grid_height - 5)]
        
        print("Firewall Defender started! Place towers to stop malware from reaching the network core!")
        
    def update(self):
        if not self.game_active:
            return
            
        self.handle_input()
        self.spawn_enemies()
        self.update_enemies()
        self.update_towers()
        self.update_projectiles()
        self.check_game_over()
        
    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        grid_x = mouse_pos[0] // self.grid_size
        grid_y = mouse_pos[1] // self.grid_size
        
        if pygame.mouse.get_pressed()[0]:  # Left click
            self.place_tower(grid_x, grid_y)
            
    def place_tower(self, x, y):
        # Check if valid position and enough money
        if (x, y) in self.path or self.money < 50:
            return
            
        # Check if position is empty
        for tower in self.towers:
            if tower['x'] == x and tower['y'] == y:
                return
                
        # Place tower
        self.towers.append({
            'x': x, 'y': y, 
            'type': 'firewall',
            'range': 3,
            'damage': 10,
            'cooldown': 0,
            'attack_speed': 1.0
        })
        self.money -= 50
        print(f"🔥 Firewall placed at ({x}, {y})! Money: {self.money}")
        
    def spawn_enemies(self):
        self.wave_timer += 1/60
        
        if len(self.enemies) == 0 and self.wave_timer > 5:
            # Spawn new wave
            for i in range(self.enemies_per_wave):
                enemy_type = random.choice(['virus', 'trojan', 'ransomware'])
                health = 30 if enemy_type == 'virus' else 50 if enemy_type == 'trojan' else 80
                speed = 0.5 if enemy_type == 'virus' else 0.3 if enemy_type == 'trojan' else 0.2
                reward = 20 if enemy_type == 'virus' else 30 if enemy_type == 'trojan' else 50
                
                self.enemies.append({
                    'type': enemy_type,
                    'health': health,
                    'max_health': health,
                    'speed': speed,
                    'position': 0,
                    'reward': reward
                })
                
            self.current_wave += 1
            self.enemies_per_wave += 2
            self.wave_timer = 0
            print(f"🚨 Wave {self.current_wave} incoming! {self.enemies_per_wave} enemies")
            
    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy['position'] += enemy['speed']
            
            # Check if enemy reached the end
            if enemy['position'] >= len(self.path) - 1:
                self.enemies.remove(enemy)
                self.lives -= 1
                print(f"💥 Malware breached! Lives: {self.lives}")
                
            # Check if enemy died
            if enemy['health'] <= 0:
                self.enemies.remove(enemy)
                self.money += enemy['reward']
                print(f"✅ Malware eliminated! +{enemy['reward']} money")
                
    def update_towers(self):
        for tower in self.towers:
            tower['cooldown'] -= 1/60
            
            if tower['cooldown'] <= 0:
                # Find target in range
                target = self.find_target_in_range(tower)
                if target:
                    self.attack(tower, target)
                    tower['cooldown'] = tower['attack_speed']
                    
    def find_target_in_range(self, tower):
        tower_x, tower_y = self.path[tower['x']] if tower['x'] < len(self.path) else (0, 0)
        
        for enemy in self.enemies:
            enemy_pos = enemy['position']
            if enemy_pos < len(self.path):
                enemy_x, enemy_y = self.path[int(enemy_pos)]
                distance = math.sqrt((tower_x - enemy_x)**2 + (tower_y - enemy_y)**2)
                
                if distance <= tower['range']:
                    return enemy
        return None
        
    def attack(self, tower, enemy):
        enemy['health'] -= tower['damage']
        
        self.projectiles.append({
            'start_x': tower['x'] * self.grid_size + self.grid_size//2,
            'start_y': tower['y'] * self.grid_size + self.grid_size//2,
            'target': enemy,
            'progress': 0,
            'speed': 0.1
        })
        
    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile['progress'] += projectile['speed']
            
            if projectile['progress'] >= 1:
                self.projectiles.remove(projectile)
                
    def check_game_over(self):
        if self.lives <= 0:
            self.game_active = False
            print(f"💀 Game Over! Final Score: {self.score}")
            self.end_game()
            
    def render(self):
        # Draw grid
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                rect = pygame.Rect(x * self.grid_size, y * self.grid_size, 
                                 self.grid_size, self.grid_size)
                pygame.draw.rect(self.screen, DARK_BLUE, rect, 1)
                
        # Draw path
        for i, (x, y) in enumerate(self.path):
            pygame.draw.rect(self.screen, GRAY, 
                           (x * self.grid_size, y * self.grid_size, 
                            self.grid_size, self.grid_size))
                            
        # Draw towers
        for tower in self.towers:
            x = tower['x'] * self.grid_size + self.grid_size//2
            y = tower['y'] * self.grid_size + self.grid_size//2
            pygame.draw.circle(self.screen, NEON_BLUE, (x, y), 15)
            
        # Draw enemies
        for enemy in self.enemies:
            pos = min(int(enemy['position']), len(self.path) - 1)
            x, y = self.path[pos]
            x = x * self.grid_size + self.grid_size//2
            y = y * self.grid_size + self.grid_size//2
            
            color = NEON_PINK if enemy['type'] == 'virus' else \
                   NEON_ORANGE if enemy['type'] == 'trojan' else \
                   NEON_PURPLE
                   
            pygame.draw.circle(self.screen, color, (x, y), 10)
            
            # Health bar
            health_ratio = enemy['health'] / enemy['max_health']
            pygame.draw.rect(self.screen, NEON_RED, 
                           (x - 15, y - 20, 30, 5))
            pygame.draw.rect(self.screen, NEON_GREEN, 
                           (x - 15, y - 20, 30 * health_ratio, 5))
                           
        # Draw projectiles
        for projectile in self.projectiles:
            start_x, start_y = projectile['start_x'], projectile['start_y']
            target_pos = min(int(projectile['target']['position']), len(self.path) - 1)
            target_x, target_y = self.path[target_pos]
            target_x = target_x * self.grid_size + self.grid_size//2
            target_y = target_y * self.grid_size + self.grid_size//2
            
            current_x = start_x + (target_x - start_x) * projectile['progress']
            current_y = start_y + (target_y - start_y) * projectile['progress']
            
            pygame.draw.circle(self.screen, NEON_YELLOW, (int(current_x), int(current_y)), 5)
            
        self.render_ui()
        
    def render_ui(self):
        font = pygame.font.Font(None, 36)
        
        # Stats
        stats = [
            f"Wave: {self.current_wave}",
            f"Lives: {self.lives}",
            f"Money: {self.money}",
            f"Towers: {len(self.towers)}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, NEON_GREEN)
            self.screen.blit(text, (SCREEN_WIDTH - 200, 20 + i*40))
            
        # Instructions
        small_font = pygame.font.Font(None, 24)
        instructions = [
            "Click to place Firewall (50 money)",
            "Stop malware from reaching the end!",
            "Viruses (Pink): Fast, Low HP",
            "Trojans (Orange): Medium",
            "Ransomware (Purple): Slow, High HP"
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, LIGHT_GRAY)
            self.screen.blit(text, (20, 20 + i*25))