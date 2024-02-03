# coding: utf-8
"""`TempFS` opener definition.
"""
import typing

from .base import Opener
from .registry import registry

if typing.TYPE_CHECKING:
    from ..tempfs import TempFS  # noqa: F401
    from .parse import ParseResult


@registry.install
class TempOpener(Opener):
    """`TempFS` opener."""

    protocols = ["temp"]

    def open_fs(
        self,
        fs_url,  # type: str
        parse_result,  # type: ParseResult
        writeable,  # type: bool
        create,  # type: bool
        cwd,  # type: str
    ):
        # type: (...) -> TempFS
        from ..tempfs import TempFS

        temp_fs = TempFS(identifier=parse_result.resource)
        return temp_fs
