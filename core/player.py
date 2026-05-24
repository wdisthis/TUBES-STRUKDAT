import time
import shutil
from core.utils import draw_header, CLEAR_SCREEN, RED, GREEN, YELLOW, CYAN, BLUE, MAGENTA, BOLD, RESET

def music_player_simulator(queue):
    if queue.size == 0:
        print(f"\n{RED}[!] Antrean putar kosong! Tambahkan lagu terlebih dahulu.{RESET}")
        time.sleep(2)
        return

    while queue.current_playback:
        current_node = queue.current_playback
        song = current_node.song
        
        # Tampilan Statis Tanpa Refresh Loop dan Tanpa Kedap-Kedip
        print(CLEAR_SCREEN)
        draw_header("SEDANG DIPUTAR (NOW PLAYING)")
        
        # Pilih warna secara konsisten berdasarkan judul lagu
        color_choices = [GREEN, YELLOW, CYAN, BLUE, MAGENTA]
        color_idx = sum(ord(char) for char in song.track_name) % len(color_choices)
        chosen_color = color_choices[color_idx]
        
        print(f"  Judul Lagu : {chosen_color}{BOLD}{song.track_name}{RESET}")
        print(f"  Artis      : {song.artists}")
        print(f"  Rilis      : {song.year}  |  BPM: {song.bpm}")
        print(f"  Streams    : {song.streams:,}")
        print("\n" + "-" * shutil.get_terminal_size().columns)
        
        print(f"{BOLD}Kontrol Pemutar:{RESET}")
        print(f"  {CYAN}[n]{RESET} Lagu Berikutnya (Next)")
        print(f"  {CYAN}[p]{RESET} Lagu Sebelumnya (Prev)")
        print(f"  {RED}[q]{RESET} Kembali ke Menu Utama")
        print("-" * shutil.get_terminal_size().columns)
        
        choice = input(f"\n{BOLD}Pilih kontrol (n/p/q): {RESET}").strip().lower()
        
        if choice == 'q':
            print(f"\n[i] Menghentikan pemutaran musik...")
            time.sleep(1)
            return
        elif choice == 'n':
            print(f"\n[→] Mengalihkan ke lagu berikutnya...")
            if current_node.next:
                queue.current_playback = current_node.next
            else:
                print(f"[i] Akhir antrean. Memutar kembali dari awal (HEAD).")
                queue.current_playback = queue.head
            time.sleep(1.2)
        elif choice == 'p':
            print(f"\n[←] Mengalihkan ke lagu sebelumnya...")
            if current_node.prev:
                queue.current_playback = current_node.prev
            else:
                print(f"[i] Awal antrean. Memutar lagu terakhir (TAIL).")
                queue.current_playback = queue.tail
            time.sleep(1.2)
        else:
            print(f"\n{RED}[!] Kontrol tidak dikenali. Gunakan n, p, atau q.{RESET}")
            time.sleep(1)
