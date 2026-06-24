# Tugas Besar Struktur Data (Kelompok 9)

Penerapan **Single Linked List (SLL)** dan **Double Linked List (DLL)** 

---

## Anggota Kelompok 9 (Kelas Struktur Data RB)

Anggota:

*   **Afghanis Nursholehatunnisa** (124450042)
*   **Siti Sarifah Sumamah** (124450015)
*   **Adinda Deswita Maharani** (124450083)
*   **Fitra** (124450102)
*   **Dimas Arya Ramadhan** (124450118)

---

## Cara Kerja Program

1.  **Pemuatan CSV ke SLL:**
    *   Program membaca file dataset `dataset/spotify-2023.csv` baris demi baris menggunakan `csv.DictReader`.
    *   Setiap baris data dikonversi menjadi objek `Song`, dibungkus ke dalam `SLLNode`, lalu disambungkan secara berurutan (*append*) pada struktur `SingleLinkedList` katalog utama.
2.  **Penelusuran Halaman Katalog:**
    *   Katalog lagu ditampilkan secara bertahap (10 baris per halaman) dengan melakukan traversal pointer dari indeks awal halaman hingga akhir batas halaman. Penekanan input `a` atau `d` akan menggeser rentang traversal ke depan atau ke belakang.
3.  **Pencarian Sekuensial (Sequential Search):**
    *   Pencarian lagu dilakukan secara linear. Program melakukan iterasi mulai dari node `head` SLL, membandingkan kata kunci pencarian dengan atribut `.track_name` atau `.artists` pada objek lagu, hingga menemui node `None` (akhir list).
4.  **Operasi Antrean Musik (Double Linked List):**
    *   Lagu yang dipilih dari katalog akan dibungkus menjadi `DLLNode` lalu dimasukkan ke dalam antrean `DoubleLinkedList`.
    *   Operasi penghapusan lagu di posisi tengah memodifikasi pointer `next` dan `prev` dari node sebelum dan sesudah secara langsung untuk menghubungkan mereka satu sama lain.
    *   Operasi pengacakan antrean (*Shuffle*) memindahkan node secara acak di memori, dan operasi bersihkan antrean (*Clear*) memutuskan pointer `head` dan `tail` menjadi `None`.
5.  **Simulasi Pemutaran Musik (Pointer Navigation):**
    *   Aplikasi memelihara pointer penunjuk `current_playback` yang menunjuk ke node aktif saat ini di dalam DLL.
    *   Navigasi ke lagu berikutnya (*Next*) menggeser pointer aktif ke `current_playback.next`, sedangkan navigasi ke lagu sebelumnya (*Prev*) menggeser pointer ke `current_playback.prev`, menghasilkan transisi bolak-balik instan.

---

## Analisis Struktur Data

### 1. Single Linked List (`core/sll.py`)
*   **Alasan Penggunaan:** Katalog lagu bertindak sebagai penyimpan data referensi utama yang bersifat statis setelah dimuat. Operasi dominan pada katalog ini adalah pembacaan berurutan (*sequential read*) seperti pencarian linear, pemuatan berkas CSV, dan navigasi data per halaman. SLL dipilih karena alokasi memori yang lebih efisien dibandingkan DLL, di mana setiap node hanya memerlukan satu pointer penunjuk (`next`) tanpa membebani overhead memori untuk pointer referensi sebelumnya.
*   **Selection Sort SLL:** Pengurutan nilai dilakukan secara in-place pada rantai list dengan membandingkan nilai stream lagu. Penukaran elemen dilakukan pada level data objek lagu (*payload data swapping*) antar node untuk mempertahankan kestabilan rantai penunjuk pointer di memori, menghasilkan kompleksitas memori tambahan sebesar $O(1)$.

### 2. Double Linked List (`core/dll.py`)
*   **Alasan Penggunaan:** Antrean putar lagu (*play queue*) memerlukan operasi penelusuran dua arah secara realtime, yaitu memutar lagu berikutnya (*Next*) atau lagu sebelumnya (*Prev*). Dengan representasi pointer referensi ganda (`next` dan `prev`) pada setiap node, program dapat memindahkan pointer pemutaran aktif (`current_playback`) ke depan atau ke belakang dalam kompleksitas waktu konstan $O(1)$ tanpa perlu memindai ulang antrean dari node HEAD.
*   **Penyambungan Ulang Pointer (Node Deletion):** Saat suatu node di tengah list antrean dihapus, dilakukan operasi penyambungan ulang pointer (*pointer re-routing*): menghubungkan pointer node sebelum (`prev.next`) langsung ke node setelah (`next.prev`), lalu melepaskan alokasi referensi node yang dihapus guna menghindari kebocoran memori.

---

## Struktur Direktori Proyek

Aplikasi dibagi secara modular ke dalam subdirektori `core/` untuk menyisakan berkas pelaksana utama di folder root:

```text
TUBES-STRUKDAT/
├── dataset/
│   └── spotify-2023.csv             # Berkas dataset Spotify (953 lagu)
├── core/                            # Paket Modul buatan sendiri
│   ├── song.py                      # Definisi kelas Song
│   ├── sll.py                       # Implementasi SLLNode & SingleLinkedList (Selection Sort)
│   ├── dll.py                       # Implementasi DLLNode & DoubleLinkedList (Shuffle)
│   ├── utils.py                     # Parser CSV, pemetaan ANSI warna, & layout header
│   └── player.py                    # Modul pemutar musik statis
├── README.md                        # Berkas dokumentasi utama (File ini)
└── main.py                          # Berkas eksekusi utama aplikasi di root
```

---

## Library Python yang Digunakan

Aplikasi diimplementasikan menggunakan standard library bawaan Python:

*   `os` & `sys`: Konfigurasi terminal (virtual sequences untuk warna ANSI), pembersihan layar terminal, dan rekonfigurasi encoding standard output ke UTF-8.
*   `csv`: Operasi pembacaan berkas dataset `.csv` menggunakan dictionary reader.
*   `random`: Pengacakan urutan elemen DLL (*shuffle*) dan pengambilan sampel indeks acak.

---

## Cara Instalasi & Menjalankan Program

### Prasyarat:
Pastikan Python versi 3.8 ke atas telah terpasang di komputer Anda.

### Langkah-langkah Menjalankan:
1.  Buka Command Prompt (CMD) atau PowerShell.
2.  Arahkan direktori terminal ke folder proyek, misal:
    ```bash
    cd D:\Project\KULYAH\TUBES-STRUKDAT
    ```
3.  Jalankan program utama:
    ```bash
    python main.py
    ```
4.  Program akan memuat dataset CSV dan menyajikan antarmuka menu CLI.

