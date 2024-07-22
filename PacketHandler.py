class GenericPDU:
    def __init__(self):
        pass


def write_packet(request, data):
    """
    Writes a packet with the given request, data, and error parts.

    Args:
        request (int): The request number (1-8).
        data (str): The data part of the packet (up to 1024 bytes).

    Returns:
        bytes: The complete packet as bytes.
    """
    error = 0
    if not (1 <= request <= 8):
        error = 1
    request_bytes = request.to_bytes(4, byteorder='big')
    data_bytes = data.encode('utf-8')
    if len(data_bytes) > 1024:
        error = 2
    data_bytes = data_bytes.ljust(1024, b'\x00')
    error_bytes = error.to_bytes(4, byteorder='big')

    packet = request_bytes + data_bytes + error_bytes
    return packet


def read_packet(packet):
    """
    Reads a packet and extracts the request, data, and error parts.

    Args:
        packet (bytes): The complete packet as bytes.

    Returns:
        tuple: A tuple containing the request (int), data (str), and error (int).
    """
    request = int.from_bytes(packet[:4], byteorder='big')
    data = packet[4:1028].rstrip(b'\x00').decode('utf-8')
    error = int.from_bytes(packet[1028:], byteorder='big')

    return request, data, error


class PinkFloydPDU(GenericPDU):
    pass
