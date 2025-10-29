games/
├── 🐍 __init__.py                # Package initialization
├── 🐍 base_game.py               # Base class for all games
├── 📁 packet_runner/             # Game 1: Catch network packets
│   ├── 🐍 __init__.py
│   ├── 🐍 packet_runner.py       # Main game class
│   ├── 🐍 player.py              # Player controller
│   ├── 🐍 packet.py              # Packet entities
│   ├── 🐍 spawner.py             # Packet spawn system
│   └── 🐍 ui.py                  # Game-specific UI
├── 📁 firewall_defender/         # Game 2: Tower defense
│   ├── 🐍 __init__.py
│   ├── 🐍 firewall_defender.py
│   ├── 🐍 tower.py               # Defense towers
│   ├── 🐍 enemy.py               # Malware enemies
│   ├── 🐍 wave_manager.py        # Enemy waves
│   └── 🐍 map.py                 # Game map
├── 📁 code_breaker/              # Game 3: Cryptography puzzles
│   ├── 🐍 __init__.py
│   ├── 🐍 code_breaker.py
│   ├── 🐍 ciphers.py             # Encryption algorithms
│   ├── 🐍 puzzle.py              # Puzzle system
│   ├── 🐍 hint_system.py         # Help system
│   └── 🐍 timer.py               # Puzzle timer
├── 📁 social_engineering/        # Game 4: Phishing detection
│   ├── 🐍 __init__.py
│   ├── 🐍 social_engineering.py
│   ├── 🐍 scenario.py            # Phishing scenarios
│   ├── 🐍 dialogue.py            # Conversation system
│   ├── 🐍 email_system.py        # Fake email generator
│   └── 🐍 scoring.py             # Detection scoring
└── 📁 ctf_racer/                 # Game 5: Racing + CTF
    ├── 🐍 __init__.py
    ├── 🐍 ctf_racer.py
    ├── 🐍 car.py                 # Player vehicle
    ├── 🐍 track.py               # Race track
    ├── 🐍 challenge.py           # CTF challenges
    ├── 🐍 powerup.py             # Game powerups
    └── 🐍 physics.py             # Simple physics
