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
