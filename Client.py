import socket
import configparser

# Configuration
config = configparser.ConfigParser()
config.read('config.ini')

SERVER_ADDRESS = config['server']['address']
SERVER_PORT = int(config['server']['port'])
BUFFER_SIZE = int(config['server']['buffer_size'])

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
    """
    Displays the menu of available commands.
    """
    print("=========================")
    for key, value in COMMANDS.items():
        print(f"{key}. {value}")
    print("=========================")


def handle_command(client_socket, command):
    """
    Handles the given command by sending it to the server and processing the response.

    Args:
        client_socket (socket.socket): The socket object for the client.
        command (str): The command to be sent to the server.
    """
    client_socket.send(command.encode())
    response = client_socket.recv(BUFFER_SIZE).decode()
    print(response)

    if command in ["2", "3", "4", "5", "6", "7"]:
        query = input("Enter your input: ").strip()
        client_socket.send(query.encode())
        response = client_socket.recv(BUFFER_SIZE).decode()
        print(response)


def main():
    """
    The main function that sets up the client socket, connects to the server, and handles user input.
    """
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

    try:
        welcome_message = client_socket.recv(BUFFER_SIZE).decode()
        print(welcome_message)

        while True:
            display_menu()
            command = input("Enter command: ").strip().lower()

            if command in COMMANDS:
                handle_command(client_socket, command)
                if command == 'exit':
                    break
            else:
                print("Invalid command. Please try again.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()

