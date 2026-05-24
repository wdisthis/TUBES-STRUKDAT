import os
import sys
import time
import shutil
import random

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

if sys.platform.startswith('win'):
    os.system('color')

# Impor Modul Core
from core.song import Song
from core.sll import SingleLinkedList
from core.dll import DoubleLinkedList
from core.utils import load_catalog, draw_header, GREEN, YELLOW, CYAN, RED, BLUE, BOLD, RESET, CLEAR_SCREEN
from core.player import music_player_simulator

# 6. MAIN APPLICATION MENU
def main():
    csv_path = os.path.join("dataset", "spotify-2023.csv")
    print(f"{YELLOW}[i] Memuat database lagu dari Spotify 2023 CSV...{RESET}")
    catalog = load_catalog(csv_path)
    
    if catalog.size == 0:
        print(f"{RED}[!] Database lagu kosong atau file CSV tidak ditemukan di: {csv_path}{RESET}")
        print(f"{YELLOW}Pastikan file dataset/spotify-2023.csv ada di folder proyek Anda.{RESET}")
        input("\nTekan Enter untuk keluar...")
        sys.exit(1)
        
    print(f"{GREEN}[OK] Berhasil memuat {catalog.size} lagu ke dalam Katalog (Single Linked List)!{RESET}")
    time.sleep(1.5)
    
    # Inisialisasi Play Queue (Double Linked List)
    play_queue = DoubleLinkedList()
    
    # State untuk katalog per halaman
    catalog_page = 0
    songs_per_page = 10
    
    while True:
        print(CLEAR_SCREEN)
        draw_header("SPOTIFY MUSIC PLAYER - TUBES STRUKDAT")
        
        # Dashboard Info Ringkas
        print(f"  {BOLD}DATABASE STATUS:{RESET}")
        print(f"  - Jumlah Lagu di Katalog (SLL) : {CYAN}{catalog.size}{RESET} lagu")
        print(f"  - Jumlah Lagu di Antrean (DLL) : {GREEN}{play_queue.size}{RESET} lagu")
        if play_queue.current_playback:
            print(f"  - Lagu Sedang Aktif            : {YELLOW}{play_queue.current_playback.song.track_name} - {play_queue.current_playback.song.artists}{RESET}")
        else:
            print(f"  - Lagu Sedang Aktif            : {RED}Tidak Ada{RESET}")
        print("\n" + "=" * shutil.get_terminal_size().columns + "\n")
        
        print(f"  {BOLD}MENU UTAMA:{RESET}")
        print(f"  {GREEN}[1]{RESET} Lihat Katalog Lagu (Per Halaman SLL)")
        print(f"  {GREEN}[2]{RESET} Cari Lagu di Katalog (Pencarian SLL)")
        print(f"  {GREEN}[3]{RESET} Tampilkan Antrean Putar Aktual (Visualisasi DLL)")
        print(f"  {GREEN}[4]{RESET} Kelola Antrean (Tambah, Hapus, Acak, Bersihkan)")
        print(f"  {GREEN}[5]{RESET} {BOLD}{CYAN}Putar Musik (Mulai Player){RESET}")
        print(f"  {GREEN}[6]{RESET} Urutkan Katalog Berdasarkan Terpopuler (Selection Sort SLL)")
        print(f"  {GREEN}[7]{RESET} Tambah 5 Lagu Acak dari Katalog ke Antrean")
        print(f"  {RED}[8] Keluar Aplikasi{RESET}")
        
        choice = input(f"\n{BOLD}Pilih menu (1-8): {RESET}").strip()
        
        if choice == '1':
            # Tampilan Katalog Lagu Per Halaman SLL
            while True:
                print(CLEAR_SCREEN)
                draw_header(f"KATALOG LAGU - HALAMAN {catalog_page + 1}")
                
                total_pages = (catalog.size + songs_per_page - 1) // songs_per_page
                start_idx = catalog_page * songs_per_page
                
                print(f"{BOLD}{'No':<5} | {'Judul Lagu':<40} | {'Artis':<30} | {'Tahun':<6} | {'Streams':<15}{RESET}")
                print("-" * shutil.get_terminal_size().columns)
                
                for i in range(songs_per_page):
                    curr_idx = start_idx + i
                    if curr_idx >= catalog.size:
                        break
                    song = catalog.get_at_index(curr_idx)
                    if song:
                        # Potong string jika terlalu panjang agar rapi di terminal
                        title_fmt = song.track_name[:37] + '...' if len(song.track_name) > 40 else song.track_name
                        artists_fmt = song.artists[:27] + '...' if len(song.artists) > 30 else song.artists
                        print(f"{curr_idx + 1:<5} | {title_fmt:<40} | {artists_fmt:<30} | {song.year:<6} | {song.streams:,}")
                
                print("-" * shutil.get_terminal_size().columns)
                print(f"Halaman {catalog_page + 1} dari {total_pages} (Total: {catalog.size} lagu)")
                print(f"\n{BOLD}Kontrol Navigasi SLL:{RESET}")
                print(f"  {CYAN}[a]{RESET} Halaman Selanjutnya (Next) |  {CYAN}[d]{RESET} Halaman Sebelumnya (Prev)")
                print(f"  {GREEN}[t]{RESET} Tambahkan Lagu ke Antrean  |  {RED}[q]{RESET} Kembali ke Menu Utama")
                
                nav = input(f"\nPilih aksi navigasi: {RESET}").strip().lower()
                if nav == 'a':
                    if catalog_page < total_pages - 1:
                        catalog_page += 1
                elif nav == 'd':
                    if catalog_page > 0:
                        catalog_page -= 1
                elif nav == 't':
                    try:
                        no_lagu = int(input(f"Masukkan nomor lagu untuk ditambahkan (1-{catalog.size}): "))
                        idx = no_lagu - 1
                        song_to_add = catalog.get_at_index(idx)
                        if song_to_add:
                            play_queue.append(song_to_add)
                            print(f"{GREEN}[OK] Berhasil menambahkan '{song_to_add.track_name}' ke Antrean!{RESET}")
                        else:
                            print(f"{RED}[!] Nomor lagu tidak valid!{RESET}")
                    except ValueError:
                        print(f"{RED}[!] Input harus berupa angka!{RESET}")
                    time.sleep(1.5)
                elif nav == 'q':
                    break

        elif choice == '2':
            # Pencarian SLL
            while True:
                print(CLEAR_SCREEN)
                draw_header("PENCARIAN LAGU (SINGLE LINKED LIST)")
                print(f"Ketik {RED}q{RESET} untuk kembali ke Menu Utama.\n")
                query = input("Masukkan Judul Lagu atau Nama Artis yang dicari: ").strip()
                
                if query.lower() == 'q':
                    break
                    
                if not query:
                    print(f"{RED}[!] Query pencarian tidak boleh kosong!{RESET}")
                    time.sleep(1.5)
                    continue
                    
                print(f"\n{YELLOW}Mencari di Single Linked List...{RESET}")
                results = catalog.search(query)
                
                if not results:
                    print(f"\n{RED}[!] Lagu dengan kata kunci '{query}' tidak ditemukan.{RESET}")
                    input(f"\nTekan Enter untuk mencoba mencari lagi...")
                else:
                    print(f"\n{GREEN}[OK] Ditemukan {len(results)} lagu yang cocok:{RESET}\n")
                    print(f"{BOLD}{'No':<6} | {'Judul Lagu':<40} | {'Artis':<30} | {'Streams':<15}{RESET}")
                    print("-" * shutil.get_terminal_size().columns)
                    
                    for idx, (original_idx, song) in enumerate(results):
                        title_fmt = song.track_name[:37] + '...' if len(song.track_name) > 40 else song.track_name
                        artists_fmt = song.artists[:27] + '...' if len(song.artists) > 30 else song.artists
                        print(f"[{idx + 1}] ({original_idx + 1}) | {title_fmt:<40} | {artists_fmt:<30} | {song.streams:,}")
                    
                    print("-" * shutil.get_terminal_size().columns)
                    add_choice = input(f"\nIngin menambahkan salah satu lagu di atas ke antrean? (y/n): ").strip().lower()
                    if add_choice == 'y':
                        try:
                            pilihan = int(input(f"Pilih No Urutan Hasil Pencarian (1-{len(results)}): "))
                            if 1 <= pilihan <= len(results):
                                selected_song = results[pilihan - 1][1]
                                play_queue.append(selected_song)
                                print(f"{GREEN}[OK] Berhasil menambahkan '{selected_song.track_name}' ke Antrean!{RESET}")
                            else:
                                print(f"{RED}[!] Pilihan di luar jangkauan!{RESET}")
                        except ValueError:
                            print(f"{RED}[!] Input tidak valid!{RESET}")
                        time.sleep(1.5)
                    
                    again = input(f"\nApakah Anda ingin mencari lagu lain? (y/n): ").strip().lower()
                    if again != 'y':
                        break

        elif choice == '3':
            # Visualisasi Antrean DLL
            print(CLEAR_SCREEN)
            draw_header("VISUALISASI ANTREAN (DOUBLE LINKED LIST)")
            
            if play_queue.size == 0:
                print(f"\n{RED}[!] Antrean saat ini kosong.{RESET}")
                print(f"Tambahkan beberapa lagu terlebih dahulu melalui menu Katalog [1] atau Pencarian [2].")
            else:
                print(f"{BOLD}Daftar Antrean Putar (Total: {play_queue.size} lagu):{RESET}\n")
                current = play_queue.head
                idx = 1
                while current:
                    now_playing_marker = f"{CYAN}[SEDANG DIPUTAR]{RESET}" if play_queue.current_playback == current else ""
                    print(f"  [{idx}] {GREEN}{current.song.track_name}{RESET} - {current.song.artists}  {now_playing_marker}")
                    current = current.next
                    idx += 1
                
                # Visualisasi Pointer DLL <=>
                print("\n" + "-" * shutil.get_terminal_size().columns)
                print(f"{BOLD}Representasi Pointer Struktur Data Double Linked List (DLL):{RESET}\n")
                
                current = play_queue.head
                dll_visual = []
                while current:
                    dll_visual.append(f"[{current.song.track_name[:15]}]")
                    current = current.next
                
                # Render visualisasi DLL
                connector = f" {CYAN}<=> {RESET} "
                print(f" {GREEN}HEAD{RESET} ===> " + connector.join(dll_visual) + f" <=== {GREEN}TAIL{RESET}")
                print("\n" + "-" * shutil.get_terminal_size().columns)
                print(f"{YELLOW}* Keterangan: Struktur Double Linked List mendukung navigasi bolak-balik (Prev <=> Next) secara realtime.{RESET}")
                
            input(f"\nTekan Enter untuk kembali ke Menu Utama...")

        elif choice == '4':
            # Manajemen Antrean
            while True:
                print(CLEAR_SCREEN)
                draw_header("KELOLA ANTREAN (DOUBLE LINKED LIST)")
                print(f"Jumlah Lagu di Antrean saat ini: {GREEN}{play_queue.size}{RESET}\n")
                
                print(f"  {CYAN}[1]{RESET} Tambah Lagu ke Antrean (Pilih dari Katalog)")
                print(f"  {CYAN}[2]{RESET} Hapus Lagu dari Antrean")
                print(f"  {CYAN}[3]{RESET} Acak Antrean (Shuffle DLL)")
                print(f"  {CYAN}[4]{RESET} Bersihkan Semua Antrean (Clear DLL)")
                print(f"  {RED}[5] Kembali ke Menu Utama{RESET}")
                
                act = input(f"\nPilih menu kelola (1-5): ").strip()
                if act == '1':
                    print(f"\n{YELLOW}Membuka Katalog Lagu...{RESET}")
                    time.sleep(0.5)
                    break # Keluar ke menu katalog (SLL)
                elif act == '2':
                    if play_queue.size == 0:
                        print(f"\n{RED}[!] Antrean kosong, tidak ada lagu untuk dihapus!{RESET}")
                        time.sleep(1.5)
                        continue
                    
                    # Tampilkan daftar antrean singkat untuk dipilih
                    print(f"\n{BOLD}Pilih lagu yang ingin dihapus:{RESET}")
                    current = play_queue.head
                    idx = 1
                    while current:
                        print(f"  [{idx}] {current.song.track_name} - {current.song.artists}")
                        current = current.next
                        idx += 1
                        
                    try:
                        del_idx = int(input(f"\nMasukkan nomor lagu yang ingin dihapus (1-{play_queue.size}): ")) - 1
                        if play_queue.remove_at_index(del_idx):
                            print(f"\n{GREEN}[OK] Lagu berhasil dihapus dari antrean!{RESET}")
                        else:
                            print(f"\n{RED}[!] Gagal menghapus lagu. Indeks salah.{RESET}")
                    except ValueError:
                        print(f"\n{RED}[!] Input harus berupa angka!{RESET}")
                    time.sleep(1.5)
                elif act == '3':
                    if play_queue.size <= 1:
                        print(f"\n{RED}[!] Minimal harus ada 2 lagu untuk mengacak antrean!{RESET}")
                    else:
                        print(f"\n{YELLOW}Mengacak antrean...{RESET}")
                        play_queue.shuffle()
                        print(f"{GREEN}[OK] Antrean Double Linked List berhasil diacak (shuffled)!{RESET}")
                    time.sleep(1.5)
                elif act == '4':
                    print(f"\n{YELLOW}Membersihkan antrean...{RESET}")
                    play_queue.clear()
                    print(f"{GREEN}[OK] Antrean berhasil dikosongkan!{RESET}")
                    time.sleep(1.5)
                elif act == '5':
                    break

        elif choice == '5':
            # Putar Musik (Static Controller)
            music_player_simulator(play_queue)

        elif choice == '6':
            # Urutkan SLL berdasarkan streams (Popularitas)
            print(CLEAR_SCREEN)
            draw_header("PENGURUTAN DATABASE LAGU (SELECTION SORT SLL)")
            print(f"{YELLOW}Sedang mengurutkan seluruh database ({catalog.size} lagu) berdasarkan Streams terbanyak...{RESET}")
            print(f"{YELLOW}Prosedur: Melakukan Selection Sort dengan pertukaran SLL...{RESET}")
            
            start_time = time.time()
            catalog.sort_by_streams()
            duration = time.time() - start_time
            
            print(f"\n{GREEN}[OK] Sukses! Database Single Linked List berhasil diurutkan.{RESET}")
            print(f"{CYAN}Waktu eksekusi sorting: {duration:.4f} detik.{RESET}")
            print(f"\nLagu Terpopuler saat ini berada di baris awal katalog!")
            time.sleep(2)
            catalog_page = 0  # Reset halaman catalog ke awal

        elif choice == '7':
            if catalog.size < 5:
                print(f"\n{RED}[!] Database katalog tidak memiliki cukup lagu (minimal 5)!{RESET}")
            else:
                print(f"\n{YELLOW}Mengambil 5 lagu acak dari katalog Spotify...{RESET}")
                chosen_indexes = random.sample(range(catalog.size), 5)
                print(f"\n{GREEN}[OK] Berhasil menambahkan 5 lagu acak berikut ke antrean:{RESET}\n")
                for idx in chosen_indexes:
                    song = catalog.get_at_index(idx)
                    play_queue.append(song)
                    print(f"  - {GREEN}{song.track_name}{RESET} - {song.artists}")
            input(f"\nTekan Enter untuk melanjutkan...")

        elif choice == '8':
            print(CLEAR_SCREEN)
            draw_header("TERIMA KASIH")
            print("\n" + "=" * shutil.get_terminal_size().columns)
            time.sleep(1.5)
            break
        else:
            print(f"\n{RED}[!] Pilihan tidak valid. Silakan masukkan angka 1-8.{RESET}")
            time.sleep(1.5)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}[!] Program dihentikan secara paksa.{RESET}")
        sys.exit(0)
