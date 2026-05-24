import os
import csv
import shutil
from core.song import Song
from core.sll import SingleLinkedList

# Konstanta Warna ANSI untuk Visualisasi Premium
GREEN = "\033[92m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
RED = "\033[91m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RESET = "\033[0m"
CLEAR_SCREEN = "\033[2J\033[H"

def load_catalog(file_path):
    catalog = SingleLinkedList()
    if not os.path.exists(file_path):
        return catalog

    encodings = ['utf-8', 'latin-1', 'cp1252']
    success = False
    
    for encoding in encodings:
        try:
            with open(file_path, mode='r', encoding=encoding) as f:
                reader = csv.DictReader(f)
                for row in reader:
                    track_name = row.get('track_name', 'Unknown')
                    artists = row.get('artist(s)_name', 'Unknown')
                    bpm = row.get('bpm', '120')
                    streams = row.get('streams', '0')
                    year = row.get('released_year', '2023')
                    
                    song = Song(track_name, artists, bpm, streams, year)
                    catalog.append(song)
            success = True
            break
        except (UnicodeDecodeError, KeyError):
            continue
            
    return catalog

def draw_header(title):
    terminal_width = shutil.get_terminal_size().columns
    print(f"{CYAN}{BOLD}" + "=" * terminal_width + f"{RESET}")
    padding = (terminal_width - len(title) - 4) // 2
    print(" " * padding + f"{GREEN}{BOLD}[ {title} ]{RESET}")
    print(f"{CYAN}{BOLD}" + "=" * terminal_width + f"{RESET}\n")
