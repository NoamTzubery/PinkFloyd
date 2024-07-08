def parse_database_file(database_file):
    albums = []

    with open(database_file, 'r', encoding='utf-8') as f:
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

    return albums
