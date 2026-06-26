Hypixel BedWars Stats Query Tool

A lightweight, keyboard-driven GUI application for querying Hypixel BedWars statistics of Minecraft players, featuring real-time input capture, automatic UUID resolution, and intuitive stat calculation based on Hypixel's experience formula. Designed for quick access to core BedWars metrics without navigating the Hypixel website or in-game menus.
Disclaimer

This tool was developed with a focus on simplicity and accessibility for casual Minecraft players. It relies on public Mojang and Hypixel APIs, and while efforts have been made to handle edge cases (e.g., missing player data, division by zero errors), API rate limits, server outages, or changes to Hypixel's stat structure may affect functionality. The code uses threading to prevent GUI freezes and implements basic error handling, but limited testing across all environments means unexpected issues may occur. Contributions to improve reliability or add features (e.g., caching, multi-language support) are welcome.
Quick Start
For Users
Prerequisites
Install Python 3.8+ (https://www.python.org/downloads/)
Install required dependencies via command prompt/terminal:
bash
运行
pip install requests keyboard tkinter
Obtain a valid Hypixel API key (https://developer.hypixel.net/) – replace the placeholder key in the config section of the script with your own.
Run the Tool
Download the script file (e.g., bedwars_stats.py)
Execute the script:

Core metrics are calculated with safety checks to avoid division-by-zero errors:
KDR: Kills / Deaths (0 if no deaths)
FKDR: Final Kills / Final Deaths (0 if no final deaths)
WLR: Wins / Losses (0 if no losses)
Level: Derived from total BedWars experience via getBWStar()
GUI & Keyboard Handling
The tool uses tkinter for a lightweight GUI and the keyboard library for global hotkey detection. Threading is used to:
Run keyboard listening in the background (avoids blocking the GUI)
Execute API queries outside the main GUI thread (prevents freezes during network requests)
Update the GUI safely via root.after() to comply with tkinter’s thread rules
Troubleshooting
No GUI window appears: Ensure tkinter is installed (included with most Python distributions; on Linux, install via sudo apt-get install python3-tk)
"API request failed" errors: Verify your Hypixel API key is valid, not rate-limited, and the Hypixel API is online (check https://status.hypixel.net/)
Keyboard shortcuts not working: Run the script as Administrator (required for global keyboard hooks on Windows)
Division by zero warnings: The tool automatically returns 0 for stats like KDR/WLR if the denominator is 0 (no action needed)
GUI freezes: The threading implementation prevents this, but if it occurs, close the script and restart (check for unhandled API timeouts)
This tool is designed to be a no-fuss solution for quick BedWars stat checks, prioritizing ease of use over advanced features. It requires no complex setup and works with any Minecraft username, as long as the player has public Hypixel stats and a valid API key is provided.
