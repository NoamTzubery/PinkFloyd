import socket
import threading
from Data import parse_database_file

# Constants
DATABASE_FILE = "Pink_Floyd_DB.txt"
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1024
WELCOME_MESSAGE = b"Welcome to the Pink Floyd server. Please choose a command.\n"
GOODBYE_MESSAGE = b"Goodbye!"
INVALID_COMMAND_MESSAGE = b"Invalid command. Please try again.\n"

# Load albums
albums = parse_database_file(DATABASE_FILE)


def handle_list_albums():
    return [album['name'] for album in albums]


def handle_list_songs_in_album(album_name):
    for album in albums:
        if album['name'].lower() == album_name.lower():
            return [song['name'] for song in album['songs']]
    return None


def get_song_detail(song_name, detail):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return song.get(detail, "Detail not found.")
    return "Song not found."


def handle_album_of_song(song_name):
    for album in albums:
        for song in album['songs']:
            if song['name'].lower() == song_name.lower():
                return album['name']
    return None


def handle_search_song(query, key):
    results = []
    for album in albums:
        for song in album['songs']:
            if query.lower() in song[key].lower():
                results.append(song['name'])
    return results


def send_response(client_socket, response):
    client_socket.send(response.encode())


def receive_input(client_socket, prompt=None):
    if prompt:
        client_socket.send(prompt.encode())
    return client_socket.recv(BUFFER_SIZE).decode().strip()


def handle_client(client_socket):
    client_socket.send(WELCOME_MESSAGE)

    while True:
        command = receive_input(client_socket)

        if command == "1":
            albums_list = handle_list_albums()
            response = "Albums list:\n" + "\n".join(albums_list)
            send_response(client_socket, response)

        elif command == "2":
            album_name = receive_input(client_socket, "Enter the album name:\n")
            songs_list = handle_list_songs_in_album(album_name)
            response = f"Songs in '{album_name}':\n" + "\n".join(
                songs_list) if songs_list else f"No album found with the name '{album_name}'."
            send_response(client_socket, response)

        elif command == "3":
            song_name = receive_input(client_socket, "Enter the song name:\n")
            response = get_song_detail(song_name, 'duration')
            send_response(client_socket, response)

        elif command == "4":
            song_name = receive_input(client_socket, "Enter the song name:\n")
            response = get_song_detail(song_name, 'lyrics')
            send_response(client_socket, response)

        elif command == "5":
            song_name = receive_input(client_socket, "Enter the song name:\n")
            album_name = handle_album_of_song(song_name)
            if album_name:
                response = f"The song '{song_name}' is in the album '{album_name}'."
            else:
                response = f"No song found with the name '{song_name}'."
            send_response(client_socket, response)

        elif command == "6":
            query = receive_input(client_socket, "Enter the song name to search:\n")
            results = handle_search_song(query, 'name')
            response = f"Songs matching '{query}':\n" + "\n".join(
                results) if results else f"No songs found matching '{query}'."
            send_response(client_socket, response)

        elif command == "7":
            query = receive_input(client_socket, "Enter word to search song by lyrics:\n")
            results = handle_search_song(query, 'lyrics')
            response = f"Songs with lyrics matching '{query}':\n" + "\n".join(
                results) if results else f"No songs found with lyrics matching '{query}'."
            send_response(client_socket, response)

        elif command.lower() == "exit":
            client_socket.send(GOODBYE_MESSAGE)
            break

        else:
            client_socket.send(INVALID_COMMAND_MESSAGE)

    client_socket.close()


def open_connection():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server is listening on port {SERVER_PORT}...")
    return server_socket


def main():
    server_socket = open_connection()

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()