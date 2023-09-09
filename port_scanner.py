import socket
import re


def get_open_ports(target, port_range, verbose=False):
    # Get the IP address of the target
    target_ip = ""
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror:
        # If the target is not a valid IP address or hostname, return a readable error message
        if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
            return "Error: Invalid hostname"
        return "Error: Invalid IP address"
    except socket.error:
        return "Error: Invalid IP address"

    # Create a list to store open ports
    open_ports = []

    # Loop through the ports in the range
    for port in range(port_range[0], port_range[1] + 1):
        # Create a new socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Set the timeout
        socket.setdefaulttimeout(1)

        # Attempt to connect to the target IP address and port
        result = s.connect_ex((target_ip, port))

        # If the connection was successful, append the port to the list of open ports
        if result == 0:
            open_ports.append(port)

        # Close the socket
        s.close()

    # Attempt to get the hostname for the target IP address
    host = None
    try:
        host = socket.gethostbyaddr(target_ip)[0]
    except socket.herror:
        host = None

    # If verbose is True, return a readable string with the open ports and their services
    if verbose:
        if host is None:
            return f"Open ports for {target_ip}\nPORT     SERVICE\n" + "\n".join(
                [f"{port:<9}{socket.getservbyport(port)}" for port in open_ports]
            )
        return f"Open ports for {host} ({target_ip})\nPORT     SERVICE\n" + "\n".join(
            [f"{port:<9}{socket.getservbyport(port)}" for port in open_ports]
        )
    
    # If verbose is False, return the list of open ports
    return open_ports







