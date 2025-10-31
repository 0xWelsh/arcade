"""
handles dependency checking and provides a clean way to state hte game
"""

import os
import sys
import subprocess

def check_dependencies():
    """check if required packages are installed"""
    required_packages = ['pygame', 'numpy', 'Pillow']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    return missing_packages

def install_packages(packages):
    """install missing packages using pip"""
    if not missing_packages:
        return True
    
    print(f"Installing missing packages: {', '.join(missing_packages)}")

    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install'
        ] + missing_packages)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """main launcher function"""
    print("Cyberpunk Arcade - Launcher")
    print("=" * 40)

    # check dependencies
    missing = check_dependencies()

    if missing:
        print(f"Missing dependencies: {', '.join(missing)}")
        choice = input("Would you like to install them automatically (y/n): ")

        if choice.lower() in ['y', 'yes']:
            if install_packages(missing):
                print("All dependencies installed successfully.")
            else:
                print("Failed to install some dependencies. Please install them manually.")
                print(f"pip install {' '.join(missing)}")
                input("Press Enter to exit...")
                return
        else:
            print("Please install the required packages manually:")
            print(f"pip install {' '.join(missing)}")
            input("Press Enter to exit...")
            return
        
    else:
        print("All dependencies are satisfied.")

        # check if the main game file is there
        if not os.path.exists("main.py"):
            print("Error: main.py not found!")
            print("Please make sure you are running this from the game root directory.")
            input("Press Enter to exit...")
            return
        
        # launch the game
        print("\n Starting CyberPunk arcade...")
        print("=" * 40)

        try:
            from main import main as game_main
            game_main()
        except KeyboardInterrupt:
            print(f"\n Game closed by user")
        except Exception as e:
            print(f"\n Error launching game: {e}")
            input("Press Enter to exit...")


    if __name__ == "__main__":
        main()

