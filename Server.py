import socket
import threading
from Data import parse_database_file
import configparser
from ReadPacket import read_packet
from WritePacket import write_packet

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

SERVER_ADDRESS = config['server']['address']
SERVER_PORT = int(config['server']['port'])
DATABASE_FILE = "Pink_Floyd_DB.txt"
BUFFER_SIZE = 1032  # Increased buffer size to match packet size
WELCOME_MESSAGE = b"Welcome to the Pink Floyd server. Please choose a command.\n"
GOODBYE_MESSAGE = b"Goodbye!"
INVALID_COMMAND_MESSAGE = b"Invalid command. Please try again.\n"

# Load albums
albums = parse_database_file(DATABASE_FILE)


def get_albums():
    return "Albums list:\n" + "\n".join(album['name'] for album in albums)


def get_album_songs(album_name):
    for album in albums:
        if album['name'].lower() == album_name.lower():
            return "\n".join(song['name'] for song in album['songs'])
    return "-1"


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
    return "-1"


def handle_search_song(query, key):
    results = []
    for album in albums:
        for song in album['songs']:
            if query.lower() in song[key].lower():
                results.append(song['name'])
    return "\n".join(results) if results else "-1"


def handle_client(client_socket):
    client_socket.send(WELCOME_MESSAGE)
    while True:
        packet = client_socket.recv(BUFFER_SIZE)
        request_code, data, error_code = read_packet(packet)
        if request_code == 8:
            break
        elif request_code == 1:
            msg = get_albums()
            album_packet = write_packet(0, msg)
            client_socket.send(album_packet)
        else:
            if request_code == 2:
                msg = get_album_songs(data)
            elif request_code == 3:
                msg = get_song_detail(data, 'duration')
            elif request_code == 4:
                msg = get_song_detail(data, 'lyrics')
            elif request_code == 5:
                msg = handle_album_of_song(data)
            elif request_code == 6:
                msg = handle_search_song(data, 'name')
            elif request_code == 7:
                msg = handle_search_song(data, 'lyrics')

            packet = write_packet(0, msg)
            client_socket.send(packet)
    client_socket.send(GOODBYE_MESSAGE)
    client_socket.close()


def open_connection():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, SERVER_PORT))
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
