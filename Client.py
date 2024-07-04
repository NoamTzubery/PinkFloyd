# client.py
import socket


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    try:
        while True:
            welcome_message = client_socket.recv(1024).decode()
            print(welcome_message)

            while True:
                print("=========================")
                print("1. List of albums")
                print("2. Songs in an album")
                print("3. Length of a song")
                print("4. Lyrics of a song")
                print("5. Find album of a song")
                print("6. Search song by name")
                print("7. Search song by lyrics")
                print("Type 'exit' to quit")
                print("=========================")

                command = input("Enter command: ")

                client_socket.send(command.encode())

                if command == "1":
                    response = client_socket.recv(1024).decode()
                    print(response)

                elif command == "2":
                    album_name = input("Enter the album name: ")
                    client_socket.send(album_name.encode())
                    response = client_socket.recv(1024).decode()
                    print(response)

                elif command == "3":
                    song_name = input("Enter the song name: ")
                    client_socket.send(song_name.encode())
                    response = client_socket.recv(1024).decode()
                    print(response)

                elif command == "4":
                    song_name = input("Enter the song name: ")
                    client_socket.send(song_name.encode())
                    response = client_socket.recv(1024).decode()
                    print(response)

                elif command == "5":
                    song_name = input("Enter the song name: ")
                    client_socket.send(song_name.encode())
                    response = client_socket.recv(1024).decode()
                    print(response)

                elif command == "6":
                    query = input("Enter the song to search: ")
                    client_socket.send(query.encode())
                    response = client_socket.recv(1024).decode()
                    print(response)

                elif command == "7":
                    query = input("Enter word to search song by: ")
                    client_socket.send(query.encode())
                    response = client_socket.recv(1024).decode()
                    print(response)

                elif command.lower() == "exit":
                    response = client_socket.recv(1024).decode()
                    print(response)
                    break

                else:
                    response = client_socket.recv(1024).decode()
                    print(response)

    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
