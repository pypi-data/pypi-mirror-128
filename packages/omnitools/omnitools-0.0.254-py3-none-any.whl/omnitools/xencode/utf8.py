from ..xtype import *


def utf8e(s: str) -> bytes:
    return s.encode("utf-8")


def utf8d(b: bytes) -> str:
    return b.decode("utf-8")


def try_utf8d(b: str_or_bytes) -> str:
    try:
        return utf8d(b)
    except:
        return b


def try_utf8e(s: str_or_bytes) -> bytes:
    try:
        return utf8e(s)
    except:
        return s


FULL2HALF = dict((i + 0xFEE0, i) for i in range(0x21, 0x7F))
FULL2HALF[0x3000] = 0x20
HALF2FULL = dict((i, i + 0xFEE0) for i in range(0x21, 0x7F))
HALF2FULL[0x20] = 0x3000


def f2h_width(s):
    return str(s).translate(FULL2HALF)


def h2f_width(s):
    return str(s).translate(HALF2FULL)


