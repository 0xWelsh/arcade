# games/social_engineering/social_engineering.py
import pygame
import random
from games.base_game import BaseGame
from config import *

class SocialEngineering(BaseGame):
    def __init__(self, game_engine):
        super().__init__(game_engine)
        self.game_active = True
        self.current_scenario = None
        self.scenarios_completed = 0
        self.correct_answers = 0
        
        self.load_scenario()
        print("Social Engineering Sim started! Identify phishing attempts and social engineering tricks!")
        
    def load_scenario(self):
        scenarios = [
            {
                'type': 'phishing_email',
                'title': 'Suspicious Email',
                'content': '''From: security@your-bank.com
Subject: Urgent: Your Account Will Be Suspended

Dear Customer,

We detected unusual activity on your account. To prevent suspension, verify your identity immediately.

Click here: http://fake-bank-security.com/verify

Bank Security Team''',
                'question': 'Is this email legitimate?',
                'options': ['Yes - It looks official', 'No - Suspicious link and urgency'],
                'correct': 1,
                'explanation': 'This is phishing! Legitimate banks never ask for verification via email links.'
            },
            {
                'type': 'tech_support',
                'title': 'Phone Call',
                'content': '''Caller: "Hello, I'm from Microsoft Support. We detected viruses on your computer. Please install this remote access tool so I can fix it."''',
                'question': 'How should you respond?',
                'options': ['Install the tool - They sound professional', 'Hang up - This is a tech support scam'],
                'correct': 1,
                'explanation': 'Tech support scams use fear to gain remote access to your computer.'
            },
            {
                'type': 'social_media',
                'title': 'Social Media Message',
                'content': '''Message from "friend": "Hey! Check out this crazy video of you: http://bit.ly/suspicious-link"''',
                'question': 'What should you do?',
                'question': 'Is this safe to click?',
                'options': ['Click it - It\'s from a friend', 'Ignore it - Account may be compromised'],
                'correct': 1,
                'explanation': 'Compromised accounts often send malicious links to friends.'
            }
        ]
        
        self.current_scenario = random.choice(scenarios)
        
    def handle_input(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        
        # Create option buttons
        option_rects = []
        for i, option in enumerate(self.current_scenario['options']):
            rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 300 + i*80, 400, 60)
            option_rects.append(rect)
            
            if mouse_click and rect.collidepoint(mouse_pos):
                self.check_answer(i)
                
    def check_answer(self, selected_option):
        is_correct = (selected_option == self.current_scenario['correct'])
        
        if is_correct:
            self.correct_answers += 1
            self.score += 50
            print("✅ Correct! " + self.current_scenario['explanation'])
        else:
            print("❌ Wrong! " + self.current_scenario['explanation'])
            
        self.scenarios_completed += 1
        
        if self.scenarios_completed >= 5:
            accuracy = (self.correct_answers / 5) * 100
            print(f"🎯 Game Complete! Accuracy: {accuracy}%")
            self.end_game()
        else:
            self.load_scenario()
            
    def update(self):
        if not self.game_active:
            return
            
        self.handle_input()
        
    def render(self):
        if not self.current_scenario:
            return
            
        font_large = pygame.font.Font(None, 48)
        font_medium = pygame.font.Font(None, 32)
        font_small = pygame.font.Font(None, 24)
        
        # Title
        title = font_large.render("Social Engineering Sim", True, NEON_BLUE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
        
        # Scenario title
        scenario_title = font_medium.render(self.current_scenario['title'], True, NEON_GREEN)
        self.screen.blit(scenario_title, (SCREEN_WIDTH//2 - scenario_title.get_width()//2, 120))
        
        # Content
        content_lines = self.current_scenario['content'].split('\n')
        for i, line in enumerate(content_lines):
            text = font_small.render(line, True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - 300, 180 + i*25))
            
        # Question
        question = font_medium.render(self.current_scenario['question'], True, NEON_ORANGE)
        self.screen.blit(question, (SCREEN_WIDTH//2 - question.get_width()//2, 280))
        
        # Options
        for i, option in enumerate(self.current_scenario['options']):
            # Draw button
            rect = pygame.Rect(SCREEN_WIDTH//2 - 200, 320 + i*80, 400, 60)
            pygame.draw.rect(self.screen, DARK_BLUE, rect)
            pygame.draw.rect(self.screen, NEON_BLUE, rect, 2)
            
            # Draw option text
            option_text = font_medium.render(option, True, WHITE)
            self.screen.blit(option_text, (rect.centerx - option_text.get_width()//2, 
                                         rect.centery - option_text.get_height()//2))
                                         
        # Stats
        stats = font_small.render(f"Scenarios: {self.scenarios_completed}/5 | Correct: {self.correct_answers} | Score: {self.score}", True, LIGHT_GRAY)
        self.screen.blit(stats, (20, SCREEN_HEIGHT - 40))