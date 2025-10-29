"""
handles application startup and error handling
"""

import sys
import traceback
from game import CyberpunkArcade

def main():
    """
    main entry point for the game
    """

    print("=" * 50)
    print("CyberPunk Arcaede - Starting up...")
    print("=" * 50)

    game = None

    try:
        # create and run the game
        game = CyberpunkArcade()
        game.run()

    except KeyboardInterrupt:
        print("\nGame interrupted by user")

    except Exception as e:
        print(f"\n CRITICAL ERROR: {e}")
        print("\nStack trace:")
        traceback.print_exc()

        #try to save the game if possible
        if game:
            try:
                game._save_game_data()
                print("Game state saved before crash.")
            except:
                print("Could not save game state")

        input("\nPress Enter to exit...")


    finally:
        # ensure clean shutdown
        if game:
            game._quit()

    print("CyberPunk Arcade - Shutdown Complete")
    sys.exit(0)

if __name__ == "__main__":
    main()