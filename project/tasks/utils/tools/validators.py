import ipaddress


def is_ip_range(value: str):
    try:
        ipaddress.IPv4Network(value)
        return True
    except ValueError:
        return False
