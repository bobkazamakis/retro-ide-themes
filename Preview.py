"""Preview file for the retro IDE color schemes.

Open this file with each scheme to check Python coverage:
comments, docstrings, decorators, f-strings, numbers, types, and errors.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable, Optional

MAX_RETRY: int = 3          # constant in capitals
RATE = 0.075                # float
MASK = 0xFF_00             # hex with separator
PATTERN = re.compile(r"^(?P<code>[A-Z]{3})-(\d+)$")     # regular expression


class Currency(Enum):
    """An enumeration. Members show as constants."""

    EUR = "EUR"
    USD = "USD"


@dataclass(frozen=True, slots=True)
class Money:
    """A value with a currency. The decorator above is an attribute."""

    amount: float
    currency: Currency = Currency.EUR
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(f"negative amount: {self.amount!r}")

    @property
    def label(self) -> str:
        return f"{self.amount:,.2f} {self.currency.value}"      # format specifier

    def __add__(self, other: "Money") -> "Money":
        assert self.currency is other.currency, "currency mismatch"
        return Money(self.amount + other.amount, self.currency)


def total(items: Iterable[Money], *, discount: Optional[float] = None) -> Money:
    # TODO: support more than one currency
    result = Money(0.0)
    for item in items:
        result += item
    if discount is not None and 0 < discount <= 1:
        result = Money(result.amount * (1 - discount), result.currency)
    return result


async def fetch(url: str, timeout: float = 2.5) -> dict[str, object]:
    import json          # local import
    import urllib.request

    with urllib.request.urlopen(url, timeout=timeout) as response:
        payload: bytes = response.read()
    return json.loads(payload.decode("utf-8"))


try:
    print(total([Money(19.99), Money(5.01)]).label)
except (ValueError, AssertionError) as error:      # exception types
    print("failed:", error, sep=" ")
finally:
    del MASK

lambda_sum = lambda a, b: a + b       # noqa: E731
squares = {n: n ** 2 for n in range(10) if n % 2 == 0}
text = """A triple-quoted string
with a second line."""
raw = r"C:\temp\no-escape"
