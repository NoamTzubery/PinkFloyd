# server.py
import socket
import threading
from Data import parse_database_file

database_file = "Pink_Floyd_DB.txt"

# list of all albums parsed
albums = parse_database_file(database_file)


def handle_list_albums():
    album_names = [album['name'] for album in albums]
    return album_names


def handle_list_songs_in_album(album_name):
    for album in albums:
        if album['name'].lower() == album_name.lower():
            song_names = [song['name'] for song in album['songs']]
            return song_names
    return None


def get_song_length(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song['duration']
    return "Song not found."


def get_song_lyrics(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song['lyrics']
    return "song not found."


def open_connection():
    curr_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    curr_server_socket.bind(('localhost', 12345))
    curr_server_socket.listen(5)
    print("Server is listening on port 12345...")
    return curr_server_socket


def handle_song_lyrics(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song['lyrics']
    return None


def handle_album_of_song(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return album['name']
    return None


def handle_search_song_by_name(query):
    results = []
    for album in albums:
        for song in album['songs']:
            if query.lower() in song['name'].lower():
                results.append(song['name'])
    return results


def handle_search_song_by_lyrics(query):
    results = []
    for album in albums:
        for song in album['songs']:
            if query.lower() in song['lyrics'].lower():
                results.append(song['name'])
    return results


def handle_client(client_socket):
    client_socket.send(b"Welcome to the Pink Floyd server. Please choose a command.\n")

    while True:
        command = client_socket.recv(1024).decode().strip()

        if command == "1":
            albums_list = handle_list_albums()
            response = "Albums list:\n" + "\n".join(albums_list)
            client_socket.send(response.encode())

        elif command == "2":
            client_socket.send(b"Enter the album name:\n")
            album_name = client_socket.recv(1024).decode().strip()
            songs_list = handle_list_songs_in_album(album_name)
            if songs_list is not None:
                response = f"Songs in '{album_name}':\n" + "\n".join(songs_list)
            else:
                response = f"No album found with the name '{album_name}'."
            client_socket.send(response.encode())

        elif command == "3":
            song_name = client_socket.recv(1024).decode().strip()
            response = get_song_length(song_name)
            client_socket.send(response.encode('utf-8'))

        elif command == "4":
            client_socket.send(b"Enter the song name:\n")
            song_name = client_socket.recv(1024).decode().strip()
            song_lyrics = handle_song_lyrics(song_name)
            if song_lyrics is not None:
                response = f"Lyrics of the song '{song_name}':\n{song_lyrics}"
            else:
                response = f"No song found with the name '{song_name}'."
            client_socket.send(response.encode())

        elif command == "5":
            song_name = client_socket.recv(1024).decode().strip()
            album_name = handle_album_of_song(song_name)
            if album_name is not None:
                response = f"The song '{song_name}' is in the album '{album_name}'."
            else:
                response = f"No song found with the name '{song_name}'."
            client_socket.send(response.encode())

        elif command == "6":
            query = client_socket.recv(1024).decode().strip()
            results = handle_search_song_by_name(query)
            if results:
                response = f"Songs matching '{query}':\n" + "\n".join(results)
            else:
                response = f"No songs found matching '{query}'."
            client_socket.send(response.encode())

        elif command == "7":
            query = client_socket.recv(1024).decode().strip()
            results = handle_search_song_by_lyrics(query)
            if results:
                response = f"Songs with lyrics matching '{query}':\n" + "\n".join(results)
            else:
                response = f"No songs found with lyrics matching '{query}'."
            client_socket.send(response.encode())

        elif command.lower() == "exit":
            client_socket.send(b"Goodbye!")
            break

        else:
            client_socket.send(b"Invalid command. Please try again.\n")

    client_socket.close()


def main():
    server_socket = open_connection()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            # open a thread to handle client
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
