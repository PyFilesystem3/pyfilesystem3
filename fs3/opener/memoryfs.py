# coding: utf-8
"""`MemoryFS` opener definition.
"""
import typing

from .base import Opener
from .registry import registry

if typing.TYPE_CHECKING:
    from ..memoryfs import MemoryFS  # noqa: F401
    from .parse import ParseResult


@registry.install
class MemOpener(Opener):
    """`MemoryFS` opener."""

    protocols = ["mem"]

    def open_fs(
        self,
        fs_url,  # type: str
        parse_result,  # type: ParseResult
        writeable,  # type: bool
        create,  # type: bool
        cwd,  # type: str
    ):
        # type: (...) -> MemoryFS
        from ..memoryfs import MemoryFS

        mem_fs = MemoryFS()
        return mem_fs
