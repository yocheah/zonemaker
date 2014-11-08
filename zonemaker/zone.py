import re
from ipaddress import IPv4Address, IPv6Address
from typing import List, Dict, Any


second = 1
minute = 60*second
hour = 60*minute
day = 24*hour

def hostname(name: str) -> str:
    # check hostname for validity
    label = r'[a-zA-Z90-9]([a-zA-Z90-9-]{0,61}[a-zA-Z90-9])?' # must not start or end with hyphen
    pattern = r'^{0}(\.{0})*\.?'.format(label)
    print(pattern)
    if re.match(pattern, name):
        return name
    raise Exception(name+" is not a valid hostname")

class Address:
    def __init__(self, IPv4: str = None, IPv6: str = None) -> None:
        self._IPv4 = None if IPv4 is None else IPv4Address(IPv4)
        self._IPv6 = None if IPv6 is None else IPv6Address(IPv6)
    
    def IPv4(self):
        return Address(IPv4 = self._IPv4)
    
    def IPv6(self):
        return Address(IPv6 = self._IPv6)

class Name:
    def __init__(self, address: Address = None, MX: List = None,
                 TCP: Dict[int, Any] = None, UDP: Dict[int, Any] = None) -> None:
        self._address = address

class Service:
    def __init__(self, SRV: str = None, TLSA: str=None) -> None:
        self._SRV = SRV
        self._TLSA = TLSA

class CName:
    def __init__(self, name: str) -> None:
        self._name = name

class Delegation():
    def __init__(self, NS: str, DS: str = None) -> None:
        pass

class Zone:
    def __init__(self, name: str, mail: str, NS: List[str],
                 secondary_refresh: int, secondary_retry: int, secondary_discard: int,
                 NX_TTL: int = None, A_TTL: int = None, other_TTL: int = None,
                 domains: Dict[str, Any] = {}) -> None:
        self._name = hostname(name)
        if not mail.endswith('.'): raise Exception("Mail must be absolute, end with a dot")
        atpos = mail.find('@')
        if atpos < 0 or atpos > mail.find('.'): raise Exception("Mail must contain an @ before the first dot")
        self._mail = hostname(mail.replace('@', '.', 1))
        self._NS = list(map(hostname, NS))
        
        self._secondary_refresh = secondary_refresh
        self._secondary_retry = secondary_retry
        self._secondary_discard = secondary_discard
        
        assert other_TTL is not None
        self._NX_TTL = other_TTL if NX_TTL is None else NX_TTL
        self._A_TTL = other_TTL if A_TTL is None else A_TTL
        self._other_TTL = other_TTL
    
    def write(self, file):
        raise NotImplementedError()
