class Song:
    def __init__(self, track_name, artists, bpm, streams, year):
        self.track_name = track_name
        self.artists = artists
        self.bpm = int(bpm) if bpm.isdigit() else 120
        self.year = int(year) if year.isdigit() else 2023
        
        # Streams can sometimes have non-numeric chars in some datasets
        try:
            self.streams = int(streams)
        except ValueError:
            self.streams = 0

    def get_popularity_stars(self):
        # Mengembalikan rating kepopuleran berbasis skala 5 bintang (★ dan ☆)
        if self.streams > 1000000000:
            rating = 5
        elif self.streams > 500000000:
            rating = 4
        elif self.streams > 100000000:
            rating = 3
        elif self.streams > 50000000:
            rating = 2
        else:
            rating = 1
            
        bintang = "★" * rating
        kosong = "☆" * (5 - rating)
        return f"{bintang}{kosong}"
