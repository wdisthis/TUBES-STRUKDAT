import random

class DLLNode:
    def __init__(self, song):
        self.song = song
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.current_playback = None  # Pointer untuk lagu yang sedang diputar

    def append(self, song):
        new_node = DLLNode(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1
        
        # Jika belum ada lagu yang aktif, set lagu pertama sebagai playback aktif
        if not self.current_playback:
            self.current_playback = self.head

    def remove_at_index(self, index):
        if index < 0 or index >= self.size:
            return False
        
        current = self.head
        for _ in range(index):
            current = current.next

        # Pointer re-routing
        if current == self.head:
            self.head = current.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif current == self.tail:
            self.tail = current.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
        else:
            current.prev.next = current.next
            current.next.prev = current.prev

        # Jika lagu yang dihapus sedang diputar, pindahkan playback
        if self.current_playback == current:
            self.current_playback = current.next if current.next else self.head

        self.size -= 1
        return True

    def clear(self):
        self.head = None
        self.tail = None
        self.size = 0
        self.current_playback = None

    def shuffle(self):
        if self.size <= 1:
            return
        
        # Ekstrak data ke list Python untuk diacak, lalu bangun kembali DLL
        songs_list = []
        current = self.head
        while current:
            songs_list.append(current.song)
            current = current.next
            
        random.shuffle(songs_list)
        
        self.clear()
        for s in songs_list:
            self.append(s)
