import socket
import configparser
from WritePacket import write_packet
from ReadPacket import read_packet

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
    "8": "Exit"
}


def display_menu():
    """
    Displays the menu of available commands.
    """
    print("=========================")
    for key, value in COMMANDS.items():
        print(f"{key}. {value}")
    print("=========================")


def send_and_receive_packet(client_socket, command, data=""):
    packet = write_packet(int(command), data)
    client_socket.send(packet)
    response_packet = client_socket.recv(BUFFER_SIZE)
    _, data, error = read_packet(response_packet)
    if error == 1:
        print("Invalid input")
    else:
        print(data)


def handle_command(client_socket, command):
    """
    Handles the given command by sending it to the server and processing the response.

    Args:
        client_socket (socket.socket): The socket object for the client.
        command (str): The command to be sent to the server.
    """
    if command == "1":
        send_and_receive_packet(client_socket, command)
    elif command == "2":
        album_name = input("Enter the album name: ").strip()
        send_and_receive_packet(client_socket, command, album_name)
    elif command in ["3", "4", "5"]:
        song_name = input("Enter the song name: ").strip()
        send_and_receive_packet(client_socket, command, song_name)
    elif command in ["6", "7"]:
        query = input("Enter your input: ").strip()
        send_and_receive_packet(client_socket, command, query)
    elif command == "8":
        send_and_receive_packet(client_socket, command)
        print("Goodbye!")
        return False
    return True


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
                if not handle_command(client_socket, command):
                    break
            else:
                print("Invalid command. Please try again.")
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
