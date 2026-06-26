"""
Improved bedwarsinfo.py
- Async network calls using ThreadPoolExecutor
- Read HYPIXEL_API_KEY from environment variable
- UI updates via tkinter.after to remain thread-safe
- Caching and optional auto-refresh
"""

import os
import threading
import concurrent.futures
import time
from hypixelapi import HypixelAPI
from apitools import getuuid, getBWStar
import keyboard
from tkinter import *

# Configuration
REFRESH_INTERVAL = int(os.environ.get('HS_REFRESH', '2'))  # seconds
AUTO_REFRESH = True  # set to False to only fetch on Enter
HYPIXEL_API_KEY = os.environ.get('HYPIXEL_API_KEY')

if not HYPIXEL_API_KEY:
    print("Warning: HYPIXEL_API_KEY not set in environment. Set it before running to use Hypixel API.")

executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)

# UI state
cached_text = "Press Ctrl+/ to enter player name"
cached_lock = threading.Lock()
current_player = None
stat = False
pNameInput = ''
refresh_job = None
root = None
pNameView = None
infoPrint = None


def format_stats_from_json(player_json):
    try:
        pName = player_json.get('displayname', 'Unknown')
        pBWInfo = player_json.get('stats', {}).get('Bedwars', {})
        pBWLevel = getBWStar(pBWInfo.get('Experience', 0))
        wins = pBWInfo.get('wins_bedwars', 0)
        losses = pBWInfo.get('losses_bedwars', 0)
        kills = pBWInfo.get('kills_bedwars', 0)
        deaths = pBWInfo.get('deaths_bedwars', 0)
        fk = pBWInfo.get('final_kills_bedwars', 0)
        fd = pBWInfo.get('final_deaths_bedwars', 0)

        pBWWLR = round(wins / losses, 2) if losses else wins
        pBWKDR = round(kills / deaths, 2) if deaths else kills
        pBWFKDR = round(fk / fd, 2) if fd else fk

        return f"player {pName}'s Bedwars Info\nLevel:{pBWLevel}\nKDR:{pBWKDR}\nFKDR:{pBWFKDR}\nWLR:{pBWWLR}"
    except Exception as e:
        return f"Error formatting stats: {e}"


def fetch_player_stats(player):
    """Fetch player stats from Hypixel API (runs in background thread). Returns formatted string."""
    if not HYPIXEL_API_KEY:
        return "Error: HYPIXEL_API_KEY not set in environment."
    try:
        api = HypixelAPI(HYPIXEL_API_KEY)
        uuid = getuuid(player)
        if not uuid:
            return f"Error: UUID for player '{player}' not found." 
        pInfo = api.get_player_json(uuid)
        player_json = pInfo.get('player')
        if not player_json:
            return f"Error: Player '{player}' not found on Hypixel."
        return format_stats_from_json(player_json)
    except Exception as e:
        return f"Error fetching stats: {e}"


def schedule_update(text):
    """Schedule UI update from main thread."""
    def _update():
        with cached_lock:
            global cached_text
            cached_text = text
            if infoPrint:
                infoPrint.config(text=cached_text)
    if root:
        root.after(0, _update)


def start_fetch(player_name):
    global current_player, refresh_job
    current_player = player_name
    future = executor.submit(fetch_player_stats, player_name)

    def when_done(fut):
        text = fut.result()
        schedule_update(text)

        # schedule next refresh if AUTO_REFRESH
        if AUTO_REFRESH and current_player:
            def delayed():
                # submit another fetch
                if current_player:
                    f = executor.submit(fetch_player_stats, current_player)
                    f.add_done_callback(when_done)
            # use root.after to schedule next call in main thread then submit
            if root:
                root.after(REFRESH_INTERVAL * 1000, delayed)

    future.add_done_callback(when_done)


# Keyboard input handling
stat = False
pNameInput = ''


def on_press(key):
    global stat, pNameInput
    if stat:
        key = str(key).replace('KeyboardEvent(', '').replace(' down)', '')
        if len(key) == 1:
            pNameInput += key
        elif key == 'backspace':
            pNameInput = pNameInput[:-1]
        elif key == 'enter':
            stat = False
            player = pNameInput.replace('/', '')
            pNameInput = ''
            if pNameView:
                pNameView.config(text='')
            # start background fetch
            start_fetch(player)
        if pNameView:
            pNameView.config(text=pNameInput)


def change_stat():
    global stat
    stat = not stat


def build_ui():
    global root, pNameView, infoPrint
    root = Tk()
    root.geometry('+200+200')
    root.title('bedwarsinfo')
    root.overrideredirect(True)
    root.config(bg='#114514')
    root.wm_attributes('-transparentcolor', '#114514')
    root.attributes('-topmost', 'true')
    root.attributes('-alpha', 0.9)

    pNameView = Label(root, text='', bg='#114514', font=('微软雅黑', 15, 'bold'), fg='red')
    pNameView.pack()
    infoPrint = Label(root, text=cached_text, bg='#114514', font=('DFPOP1W5-GB', 15, 'bold'), fg='green')
    infoPrint.pack()

    # small drag support
    def start_move(event):
        root.x = event.x
        root.y = event.y

    def do_move(event):
        x = root.winfo_x() - root.x + event.x
        y = root.winfo_y() - root.y + event.y
        root.geometry(f'+{x}+{y}')

    infoPrint.bind('<Button-1>', start_move)
    infoPrint.bind('<B1-Motion>', do_move)

    # right-click to close
    def on_right_click(event):
        root.destroy()
        executor.shutdown(wait=False)
    infoPrint.bind('<Button-3>', on_right_click)

    return root


def main():
    keyboard.on_press(on_press)
    keyboard.add_hotkey('ctrl+/', change_stat)

    ui = build_ui()
    # start tk mainloop
    ui.mainloop()


if __name__ == '__main__':
    main()
