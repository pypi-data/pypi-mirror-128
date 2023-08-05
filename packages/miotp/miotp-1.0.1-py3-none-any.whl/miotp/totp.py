import hashlib
import datetime
import time
import calendar
from typing import Any, Optional

from .otp import OTP


class TOTP(OTP):
    """
    Hanlder for time-based OTP counters.
    """
    def __init__(self, s: str, digits: int = 6, digest: Any = hashlib.sha1, name: Optional[str] = None, issuer: Optional[str] = None, interval: int = 30) -> None:
        """
        :param s: secret in base32 format
        :param interval: the time interval in seconds for OTP. default is 30
        :param digits: number of integers in the OTP. default is 6
        :param digest: digest function to use in hmac (sha1)
        :param name: account name
        :param issuer: issuer
        """
        self.interval = interval
        super().__init__(s, digits=digits, digest=digest, name=name, issuer=issuer)


    def now(self) -> str:
        """
        Generate the current time OTP

        :returns: OTP value
        """
        return self.generate_otp(self.timecode(datetime.datetime.now()))

    def timecode(self, for_time: datetime.datetime) -> int:
            return int(time.mktime(for_time.timetuple()) / self.interval)
