import ipaddress
import re


def is_address_or_cidr_notation(value: str):
    try:
        ipaddress.IPv4Network(value)
        return True
    except ValueError:
        return False

def is_ip_range(value):
    pattern = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])-(([0-9]|[1-9][0-9])|[1][0-9][0-9]|[2][0-5][0-5])$"
    return bool(re.match(pattern, value))

def is_valid_ip(value: str):
    return is_address_or_cidr_notation(value) or is_ip_range(value)
