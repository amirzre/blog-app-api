from string import digits
from secrets import choice


def otp_generator(size: int = 6, char: str = digits) -> str:
    return "".join(choice(char) for _ in range(size))
