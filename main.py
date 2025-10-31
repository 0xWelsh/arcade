"""
CyberPunk Arcade - Main Entry Point
Handles application startup and error handling
"""

import sys
import traceback
import pygame  # Add this import
from game import CyberpunkArcade

def main():
    """
    Main entry point for the CyberPunk Arcade game
    """
    print("=" * 50)
    print("CyberPunk Arcade - Starting Up...")
    print("=" * 50)
    
    game = None
    
    try:
        # Create and run the game
        game = CyberpunkArcade()
        game.run()
        
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        
    except Exception as e:
        # Handle any unexpected errors
        print(f"\n💥 CRITICAL ERROR: {e}")
        print("\nStack trace:")
        traceback.print_exc()
        
        # Try to save game state if possible
        if game:
            try:
                game._save_game_data()
                print("Game state saved before crash")
            except:
                print("Could not save game state")
        
        input("\nPress Enter to exit...")
        
    finally:
        # Ensure clean shutdown
        if game:
            try:
                game.quit_game()
            except:
                # Fallback cleanup
                try:
                    pygame.quit()
                except:
                    pass
        
    print("CyberPunk Arcade - Shutdown Complete")

if __name__ == "__main__":
    main()