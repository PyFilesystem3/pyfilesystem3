# coding: utf-8
"""`Opener` abstract base class.
"""

import typing

import abc

if typing.TYPE_CHECKING:
    from ..base import FS
    from .parse import ParseResult


class Opener:
    """The base class for filesystem openers.

    An opener is responsible for opening a filesystem for a given
    protocol.

    """

    protocols = []  # type: list[str]

    def __repr__(self):
        # type: () -> str
        return "<opener {!r}>".format(self.protocols)

    @abc.abstractmethod
    def open_fs(
        self,
        fs_url,  # type: str
        parse_result,  # type: ParseResult
        writeable,  # type: bool
        create,  # type: bool
        cwd,  # type: str
    ):
        # type: (...) -> FS
        """Open a filesystem object from a FS URL.

        Arguments:
            fs_url (str): A filesystem URL.
            parse_result (~fs3.opener.parse.ParseResult): A parsed
                filesystem URL.
            writeable (bool): `True` if the filesystem must be writable.
            create (bool): `True` if the filesystem should be created
                if it does not exist.
            cwd (str): The current working directory (generally only
                relevant for OS filesystems).

        Raises:
            ~fs3.opener.errors.OpenerError: If a filesystem could not
                be opened for any reason.

        Returns:
            `~fs3.base.FS`: A filesystem instance.

        """
