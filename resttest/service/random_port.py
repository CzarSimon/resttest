# Standard library
import socket


def get_random_port() -> int:
    """Gets a random unused port on localhost.
    
    :return: Unused port number.
    """
    try:
        port = _find_unused_port()
        return port
    except Exception as e:
        print(f"Failed to get unused port{e}")


def _find_unused_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 0))
    port: int = s.getsockname()[1]
    s.close()
    return port
