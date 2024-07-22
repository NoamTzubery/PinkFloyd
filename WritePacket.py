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

