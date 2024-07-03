# server.py
import socket
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


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server is listening on port 12345...")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")

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

                elif command.lower() == "exit":
                    client_socket.send(b"Goodbye!")
                    break

                else:
                    client_socket.send(b"Invalid command. Please try again.\n")

            client_socket.close()

    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
