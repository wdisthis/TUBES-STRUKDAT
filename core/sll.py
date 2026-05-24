class SLLNode:
    def __init__(self, song):
        self.song = song
        self.next = None

class SingleLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, song):
        new_node = SLLNode(song)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def get_at_index(self, index):
        if index < 0 or index >= self.size:
            return None
        current = self.head
        for _ in range(index):
            current = current.next
        return current.song

    def search(self, query):
        results = []
        current = self.head
        query = query.lower()
        index = 0
        while current:
            if query in current.song.track_name.lower() or query in current.song.artists.lower():
                results.append((index, current.song))
            current = current.next
            index += 1
        return results

    def sort_by_streams(self):
        # Menggunakan Selection Sort pada Single Linked List (Mengurutkan Populer -> Kurang Populer)
        if not self.head or not self.head.next:
            return
        
        current = self.head
        while current:
            max_node = current
            next_node = current.next
            while next_node:
                if next_node.song.streams > max_node.song.streams:
                    max_node = next_node
                next_node = next_node.next
            
            # Tukar data lagu antara current node dan max node
            if max_node != current:
                current.song, max_node.song = max_node.song, current.song
            current = current.next
