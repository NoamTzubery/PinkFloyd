import socket


def main():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    server_address = ('localhost', 12345)
    client_socket.connect(server_address)

    try:
        while True:
            # Receive welcome message from server
            welcome_message = client_socket.recv(1024).decode()
            print(welcome_message)

            while True:
                # Get user input for command
                command = input("Enter command (1 to list albums, 'exit' to quit): ")

                # Get user input for command
                command = input("=========================")
                command = input("1. List of albums")
                command = input("2. Songs in an album")
                command = input("3. Length of a song")
                command = input("4. Lyrics of a song")
                command = input("5. Find album of a song")
                command = input("6. Search song by name")
                command = input("7. Search song by lyrics")
                command = input("Type exit to exit")
                command = input("=========================\n")

                # Send command to server
                client_socket.send(command.encode())

                # Receive response from server
                response = client_socket.recv(1024).decode()
                print(response)

                # Handle exit command
                if command.lower() == 'exit':
                    break

    finally:
        # Close the socket connection
        client_socket.close()


if __name__ == "__main__":
    main()
