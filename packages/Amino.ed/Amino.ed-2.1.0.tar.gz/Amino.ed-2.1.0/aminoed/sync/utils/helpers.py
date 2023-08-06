from ujson import loads
from base64 import b64decode
from functools import reduce


def decode_sid(sid: str) -> dict:
    args = (lambda a, e: a.replace(*e), ("-+", "_/"), sid+"="*(-len(sid)%4))
    return loads(b64decode(reduce(*args).encode())[1:-20].decode())

def sid_to_uid(sid: str) -> str:
    return decode_sid(sid)["2"]

def sid_to_ip_address(sid: str) -> str:
    return decode_sid(sid)["4"]
