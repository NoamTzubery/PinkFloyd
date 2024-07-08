import socket

# Configuration
SERVER_ADDRESS = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# Commands
COMMANDS = {
    "1": "List of albums",
    "2": "Songs in an album",
    "3": "Length of a song",
    "4": "Lyrics of a song",
    "5": "Find album of a song",
    "6": "Search song by name",
    "7": "Search song by lyrics",
    "exit": "Type 'exit' to quit"
}


def display_menu():
    print("=========================")
    for key, value in COMMANDS.items():
        print(f"{key}. {value}")
    print("=========================")


def handle_command(client_socket, command):
    client_socket.send(command.encode())
    if command in ["2", "3", "4", "5", "6", "7"]:
        query = input(f"Enter the {COMMANDS[command].split(' ')[-2]}: ")
        client_socket.send(query.encode())

    response = client_socket.recv(BUFFER_SIZE).decode()
    print(response)


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    try:
        welcome_message = client_socket.recv(BUFFER_SIZE).decode()
        print(welcome_message)

        while True:
            display_menu()
            command = input("Enter command: ").strip().lower()

            if command == 'exit':
                client_socket.send(command.encode())
                response = client_socket.recv(BUFFER_SIZE).decode()
                print(response)
                break

            if command in COMMANDS:
                handle_command(client_socket, command)
            else:
                print("Invalid command. Please try again.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
