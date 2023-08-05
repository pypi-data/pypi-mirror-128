import base64
import hashlib
import hmac
from typing import Any, Optional


class OTP:
    """
    Base class for OTP handlers.
    """
    def __init__(self, s: str, digits: int = 6, digest: Any = hashlib.sha1, name: Optional[str] = None, issuer: Optional[str] = None) -> None:
        self.digits = digits
        self.digest = digest
        self.secret = s
        self.name = name or 'Secret'
        self.issuer = issuer

    def generate_otp(self, input: int) -> str:
        if input < 0:
            raise ValueError('input must be positive integer')
        hasher = hmac.new(self.byte_secret(), self.int_to_bytesstring(input), self.digest)
        hmac_hash = bytearray(hasher.digest())
        offset = hmac_hash[-1] & 0xf
        code = ((hmac_hash[offset] & 0x7f) << 24 |
                (hmac_hash[offset + 1] & 0xff) << 16 |
                (hmac_hash[offset + 2] & 0xff) << 8 |
                (hmac_hash[offset + 3] & 0xff))
        str_code = str(code % 10 ** self.digits)
        while len(str_code) < self.digits:
            str_code = '0' + str_code

        return str_code

    def byte_secret(self) -> bytes:
        secret = self.secret
        missing_padding = len(secret) % 8
        if missing_padding != 0:
            secret += '=' * (8 - missing_padding)
        return base64.b32decode(secret, casefold=True)

    @staticmethod
    def int_to_bytesstring(i: int, padding: int = 8) -> bytes:
        result = bytearray()
        while i != 0:
            result.append(i & 0xFF)
            i >>= 8
        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))
