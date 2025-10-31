# games/ctf_racer/ctf_racer.py
import pygame
import random
import math
from games.base_game import BaseGame
from config import *

class CTFRacer(BaseGame):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.game_active = True
        self.laps = 0
        self.max_laps = 3
        self.current_challenge = None
        
        # Car physics
        self.car_x = SCREEN_WIDTH // 2
        self.car_y = SCREEN_HEIGHT - 100
        self.car_speed = 0
        self.car_max_speed = 8
        self.car_acceleration = 0.2
        self.car_rotation = 0
        
        # Track
        self.track_points = self.generate_track()
        self.current_checkpoint = 0
        
        # Challenges
        self.challenges = []
        self.generate_challenges()
        
        print("CTF Racer started! Race around the track while solving cybersecurity challenges!")
        
    def generate_track(self):
        # Simple oval track
        points = []
        track_width = 200
        
        # Outer track
        for angle in range(0, 360, 10):
            rad = math.radians(angle)
            x = SCREEN_WIDTH//2 + track_width * math.cos(rad)
            y = SCREEN_HEIGHT//2 + track_width * math.sin(rad)
            points.append((x, y))
            
        return points
        
    def generate_challenges(self):
        challenge_types = ['password_crack', 'port_scan', 'forensics', 'steganography']
        
        for i in range(4):  # 4 challenges per lap
            self.challenges.append({
                'type': random.choice(challenge_types),
                'solved': False,
                'position': i * (len(self.track_points) // 4),
                'question': f"Challenge {i+1}: What is port 22 used for?",
                'answer': 'ssh',
                'options': ['HTTP', 'SSH', 'FTP', 'DNS']
            })
        
    def update(self):
        if not self.game_active:
            return
            
        self.handle_input()
        self.update_car()
        self.check_checkpoints()
        self.check_challenges()
        
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        # Acceleration
        if keys[pygame.K_UP]:
            self.car_speed = min(self.car_speed + self.car_acceleration, self.car_max_speed)
        elif keys[pygame.K_DOWN]:
            self.car_speed = max(self.car_speed - self.car_acceleration * 2, -self.car_max_speed/2)
        else:
            # Friction
            self.car_speed *= 0.95
            
        # Steering
        if keys[pygame.K_LEFT]:
            self.car_rotation -= 3
        if keys[pygame.K_RIGHT]:
            self.car_rotation += 3
            
    def update_car(self):
        # Update car position based on speed and rotation
        rad = math.radians(self.car_rotation)
        self.car_x += self.car_speed * math.sin(rad)
        self.car_y -= self.car_speed * math.cos(rad)
        
        # Keep car on screen
        self.car_x = max(50, min(SCREEN_WIDTH - 50, self.car_x))
        self.car_y = max(50, min(SCREEN_HEIGHT - 50, self.car_y))
        
    def check_checkpoints(self):
        # Simple checkpoint system based on track proximity
        car_pos = (self.car_x, self.car_y)
        
        # Find nearest track point
        min_dist = float('inf')
        nearest_index = 0
        
        for i, point in enumerate(self.track_points):
            dist = math.sqrt((car_pos[0] - point[0])**2 + (car_pos[1] - point[1])**2)
            if dist < min_dist:
                min_dist = dist
                nearest_index = i
                
        # Check if passed checkpoint
        if nearest_index > self.current_checkpoint and min_dist < 100:
            self.current_checkpoint = nearest_index
            
            # Completed lap?
            if self.current_checkpoint >= len(self.track_points) - 10:
                self.laps += 1
                self.current_checkpoint = 0
                print(f"🏁 Lap {self.laps}/{self.max_laps} completed!")
                
                if self.laps >= self.max_laps:
                    self.score += 500
                    print("🎉 Race complete! All laps finished!")
                    self.end_game()
                    
    def check_challenges(self):
        car_pos = (self.car_x, self.car_y)
        
        for challenge in self.challenges:
            if not challenge['solved']:
                challenge_pos = self.track_points[challenge['position']]
                dist = math.sqrt((car_pos[0] - challenge_pos[0])**2 + (car_pos[1] - challenge_pos[1])**2)
                
                if dist < 80:
                    self.current_challenge = challenge
                    print(f"🚩 Challenge available! {challenge['question']}")
                    break
                    
    def solve_challenge(self, answer):
        if self.current_challenge and answer.lower() == self.current_challenge['answer'].lower():
            self.current_challenge['solved'] = True
            self.score += 100
            self.car_max_speed += 1  # Speed boost for solving challenge
            print("✅ Challenge solved! Speed boost acquired!")
            self.current_challenge = None
            
            # Check if all challenges solved
            if all(challenge['solved'] for challenge in self.challenges):
                print("🎯 All challenges completed! Bonus points!")
                self.score += 200
        else:
            print("❌ Wrong answer! Try again.")
            
    def render(self):
        # Draw track
        for i in range(len(self.track_points)):
            pygame.draw.circle(self.screen, GRAY, (int(self.track_points[i][0]), int(self.track_points[i][1])), 5)
            
        # Draw challenges
        for challenge in self.challenges:
            if not challenge['solved']:
                pos = self.track_points[challenge['position']]
                color = NEON_PURPLE if challenge['type'] == 'password_crack' else \
                       NEON_ORANGE if challenge['type'] == 'port_scan' else \
                       NEON_GREEN if challenge['type'] == 'forensics' else \
                       NEON_BLUE
                pygame.draw.circle(self.screen, color, (int(pos[0]), int(pos[1])), 15)
                
        # Draw car
        car_points = self.get_car_shape()
        pygame.draw.polygon(self.screen, NEON_RED, car_points)
        
        # Draw UI
        self.render_ui()
        
    def get_car_shape(self):
        # Create car shape based on rotation
        points = []
        rad = math.radians(self.car_rotation)
        
        # Car corners relative to center
        corners = [(-20, -10), (20, -10), (20, 10), (-20, 10)]
        
        for x, y in corners:
            # Rotate point
            rotated_x = x * math.cos(rad) - y * math.sin(rad)
            rotated_y = x * math.sin(rad) + y * math.cos(rad)
            
            # Translate to car position
            points.append((self.car_x + rotated_x, self.car_y + rotated_y))
            
        return points
        
    def render_ui(self):
        font = pygame.font.Font(None, 36)
        
        # Stats
        stats = [
            f"Lap: {self.laps}/{self.max_laps}",
            f"Speed: {abs(int(self.car_speed * 10))}",
            f"Score: {self.score}",
            f"Challenges: {sum(1 for c in self.challenges if c['solved'])}/{len(self.challenges)}"
        ]
        
        for i, stat in enumerate(stats):
            text = font.render(stat, True, NEON_GREEN)
            self.screen.blit(text, (20, 20 + i*40))
            
        # Instructions
        small_font = pygame.font.Font(None, 24)
        instructions = [
            "↑ ↓ : Accelerate/Brake",
            "← → : Steer",
            "Drive near purple circles for challenges",
            "Complete 3 laps to win!"
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, LIGHT_GRAY)
            self.screen.blit(text, (SCREEN_WIDTH - 300, 20 + i*25))
            
        # Current challenge
        if self.current_challenge:
            challenge_font = pygame.font.Font(None, 28)
            challenge_text = challenge_font.render(self.current_challenge['question'], True, NEON_ORANGE)
            self.screen.blit(challenge_text, (SCREEN_WIDTH//2 - challenge_text.get_width()//2, SCREEN_HEIGHT - 100))
            
            # For demo, show answer
            answer_text = small_font.render(f"Answer: {self.current_challenge['answer']}", True, NEON_GREEN)
            self.screen.blit(answer_text, (SCREEN_WIDTH//2 - answer_text.get_width()//2, SCREEN_HEIGHT - 70))