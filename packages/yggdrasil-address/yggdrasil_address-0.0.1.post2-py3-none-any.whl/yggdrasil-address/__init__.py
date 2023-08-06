import ipaddress
import bitarray
import bitarray.util

is_nacl_installed = True
try:
    from nacl.signing import SigningKey
except ImportError:
    is_nacl_installed = False


def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')


def pk2ip(pkstr: str) -> ipaddress.IPv6Address:
    pkbits: bitarray.bitarray = bitarray.util.hex2ba(pkstr)
    if len(pkbits) != 256:
        raise RuntimeError('Wrong number of bits %d in public key "%s"' %
                           (len(pkbits), pkstr))
    nzerobits: int = pkbits.index(bitarray.bitarray('1'))
    restbits: bitarray.bitarray = pkbits[nzerobits + 1:]
    ipbits: bitarray.bitarray = (bitarray.bitarray('00000010') +
                                 bitarray.util.int2ba(nzerobits, length=8) +
                                 ~restbits[:112])
    return ipaddress.IPv6Address(ipbits.tobytes())


def ip2pk(ipv6: ipaddress.IPv6Address):
    pkbits: bitarray.bitarray = bitarray.util.zeros(256)
    ipba = bitarray.bitarray()
    ipba.frombytes(int_to_bytes(int(ipv6)))
    ipba = ipba[8:]
    height = int_from_bytes(ipba[:8].tobytes())
    pkbits[:height] = bitarray.bitarray('1' * height)
    ipba = ipba[8:]
    pkbits[height + 1:] = ipba
    pkbits_len = len(pkbits)
    pkbits = pkbits[:pkbits_len - pkbits_len % 4]
    pkbits.invert()
    return bitarray.util.ba2hex(pkbits)


def generate_sign_key():
    if not is_nacl_installed:
        print('PyNaCl is not installed. Install here https://pypi.org/project/PyNaCl/')
    return SigningKey.generate()
