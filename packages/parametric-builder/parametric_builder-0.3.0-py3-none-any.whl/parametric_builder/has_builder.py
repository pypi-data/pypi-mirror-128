from typing import Any

from parametric_builder.builder import Builder


class HasBuilder:
    """Abstract class that endows children with Builders"""

    # noinspection PyPep8Naming
    @classmethod
    def Builder(cls, **kwargs: Any) -> Builder:
        return Builder(cls, **kwargs)
