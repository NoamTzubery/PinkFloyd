import socket
from Data import parse_database_file

# Define the path to your database file
database_file = "Pink_Floyd_DB.txt"


# Function to handle the command for listing albums
def handle_list_albums():
    albums_data = parse_database_file()
    return list(albums_data.keys())


# Example of server setup and main execution loop
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
                    response = "\n".join(albums_list)
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
