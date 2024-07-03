albums = []
database_file = "Pink_Floyd_DB.txt"

with open("Pink_Floyd_DB.txt", 'r', encoding='utf-8') as f:
    current_album = None
    for line in f:
        line = line.strip()
        if line.startswith('#'):
            # New album header
            album_info = line[1:].strip().split('::')
            album_name = album_info[0]
            release_year = album_info[1]
            current_album = {
                'name': album_name,
                'year': release_year,
                'songs': []
            }
            albums.append(current_album)
        elif line.startswith('*'):
            # Song line
            if current_album is not None:
                song_info = line[1:].strip().split('::')
                song_name = song_info[0]
                composer = song_info[1]
                duration = song_info[2]
                lyrics = song_info[3]  # Assuming lyrics are included in the database
                current_album['songs'].append({
                    'name': song_name,
                    'composer': composer,
                    'duration': duration,
                    'lyrics': lyrics
                })
        else:
            # Handle unexpected lines or errors in file format
            continue

# Print the names of the albums
album_names = [album['name'] for album in albums]
print(f"The albums list: {', '.join(album_names)}")


def search_album(search_album_name):
    for album in albums:
        if album['name'].lower() == search_album_name.lower():
            for song in album['songs']:
                print(song['name'])
            return


album_to_search = input("Enter an album name: ")
search_album(album_to_search)
