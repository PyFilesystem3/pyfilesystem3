"""Manage the filesystem in a Tar archive.
"""
import typing
from typing import IO, cast

import os
import tarfile
from collections import OrderedDict

from . import errors
from ._url_tools import url_quote
from .base import FS
from .compress import write_tar
from .enums import ResourceType
from .errors import IllegalBackReference, NoURL
from .info import Info
from .iotools import RawWrapper
from .opener import open_fs
from .path import basename, frombase, isbase, normpath, parts, relpath
from .permissions import Permissions
from .wrapfs import WrapFS

if typing.TYPE_CHECKING:
    from collections.abc import Collection
    from typing import (
        Any,
        BinaryIO,
        Optional,
        Union,
    )

    from tarfile import TarInfo

    from .info import RawInfo
    from .subfs import SubFS

    T = typing.TypeVar("T", bound="ReadTarFS")


__all__ = ["TarFS", "WriteTarFS", "ReadTarFS"]


def _get_member_info(member, encoding):
    # type: (TarInfo, str) -> dict[str, object]
    # NOTE(@althonos): TarInfo.get_info is neither in the doc nor
    #     in the `tarfile` stub, and yet it exists and is public !
    return member.get_info()  # type: ignore


class TarFS(WrapFS):
    """Read and write tar files.

    There are two ways to open a `TarFS` for the use cases of reading
    a tar file, and creating a new one.

    If you open the `TarFS` with  ``write`` set to `False` (the
    default), then the filesystem will be a read only filesystem which
    maps to the files and directories within the tar file. Files are
    decompressed on the fly when you open them.

    Here's how you might extract and print a readme from a tar file::

        with TarFS('foo.tar.gz') as tar_fs:
            readme = tar_fs.readtext('readme.txt')

    If you open the TarFS with ``write`` set to `True`, then the `TarFS`
    will be a empty temporary filesystem. Any files / directories you
    create in the `TarFS` will be written in to a tar file when the `TarFS`
    is closed. The compression is set from the new file name but may be
    set manually with the ``compression`` argument.

    Here's how you might write a new tar file containing a readme.txt
    file::

        with TarFS('foo.tar.xz', write=True) as new_tar:
            new_tar.writetext(
                'readme.txt',
                'This tar file was written by PyFilesystem'
            )

    Arguments:
        file (str or io.IOBase): An OS filename, or an open file handle.
        write (bool): Set to `True` to write a new tar file, or
            use default (`False`) to read an existing tar file.
        compression (str, optional): Compression to use (one of the formats
            supported by `tarfile`: ``xz``, ``gz``, ``bz2``, or `None`).
        temp_fs (str): An FS URL or an FS instance to use to store
            data prior to tarring. Defaults to creating a new
            `~fs3.tempfs.TempFS`.

    """

    _compression_formats = {
        # FMT    #UNIX      #MSDOS
        "xz": (".tar.xz", ".txz"),
        "bz2": (".tar.bz2", ".tbz"),
        "gz": (".tar.gz", ".tgz"),
    }

    def __new__(  # type: ignore
        cls,
        file,  # type: Union[str, BinaryIO]
        write=False,  # type: bool
        compression=None,  # type: Optional[str]
        encoding="utf-8",  # type: str
        temp_fs="temp://__tartemp__",  # type: Union[str, FS]
    ):
        # type: (...) -> FS
        if isinstance(file, (str, bytes)):
            file = os.path.expanduser(file)
            filename = file  # type: str
        else:
            filename = getattr(file, "name", "")

        if write and compression is None:
            compression = None
            for comp, extensions in cls._compression_formats.items():
                if filename.endswith(extensions):
                    compression = comp
                    break

        if write:
            return WriteTarFS(
                file, compression=compression, encoding=encoding, temp_fs=temp_fs
            )
        else:
            return ReadTarFS(file, encoding=encoding)

    if typing.TYPE_CHECKING:

        def __init__(
            self,
            file,  # type: Union[str, BinaryIO]
            write=False,  # type: bool
            compression=None,  # type: Optional[str]
            encoding="utf-8",  # type: str
            temp_fs="temp://__tartemp__",  # type: str
        ):  # noqa: D107
            # type: (...) -> None
            pass


class WriteTarFS(WrapFS):
    """A writable tar file."""

    def __init__(
        self,
        file,  # type: Union[str, BinaryIO]
        compression=None,  # type: Optional[str]
        encoding="utf-8",  # type: str
        temp_fs="temp://__tartemp__",  # type: Union[str, FS]
    ):  # noqa: D107
        # type: (...) -> None
        self._file = file  # type: Union[str, BinaryIO]
        self.compression = compression
        self.encoding = encoding
        self._temp_fs_url = temp_fs
        self._temp_fs = open_fs(temp_fs)
        self._meta = dict(self._temp_fs.getmeta())  # type: ignore
        super().__init__(self._temp_fs)

    def __repr__(self):
        # type: () -> str
        t = "WriteTarFS({!r}, compression={!r}, encoding={!r}, temp_fs={!r})"
        return t.format(self._file, self.compression, self.encoding, self._temp_fs_url)

    def __str__(self):
        # type: () -> str
        return "<TarFS-write '{}'>".format(self._file)

    def delegate_path(self, path):
        # type: (str) -> tuple[FS, str]
        return self._temp_fs, path

    def delegate_fs(self):
        # type: () -> FS
        return self._temp_fs

    def close(self):
        # type: () -> None
        if not self.isclosed():
            try:
                self.write_tar()
            finally:
                self._temp_fs.close()
        super().close()

    def write_tar(
        self,
        file=None,  # type: Union[str, BinaryIO, None]
        compression=None,  # type: Optional[str]
        encoding=None,  # type: Optional[str]
    ):
        # type: (...) -> None
        """Write tar to a file.

        Arguments:
            file (str or io.IOBase, optional): Destination file, may be
                a file name or an open file object.
            compression (str, optional): Compression to use (one of
                the constants defined in `tarfile` in the stdlib).
            encoding (str, optional): The character encoding to use
                (default uses the encoding defined in
                `~WriteTarFS.__init__`).

        Note:
            This is called automatically when the TarFS is closed.

        """
        if not self.isclosed():
            write_tar(
                self._temp_fs,
                file or self._file,
                compression=compression or self.compression,
                encoding=encoding or self.encoding,
            )


class ReadTarFS(FS):
    """A readable tar file."""

    _meta = {
        "case_insensitive": True,
        "network": False,
        "read_only": True,
        "supports_rename": False,
        "thread_safe": True,
        "unicode_paths": True,
        "virtual": False,
    }

    _typemap = type_map = {
        tarfile.BLKTYPE: ResourceType.block_special_file,
        tarfile.CHRTYPE: ResourceType.character,
        tarfile.DIRTYPE: ResourceType.directory,
        tarfile.FIFOTYPE: ResourceType.fifo,
        tarfile.REGTYPE: ResourceType.file,
        tarfile.AREGTYPE: ResourceType.file,
        tarfile.SYMTYPE: ResourceType.symlink,
        tarfile.CONTTYPE: ResourceType.file,
        tarfile.LNKTYPE: ResourceType.symlink,
    }

    @errors.CreateFailed.catch_all
    def __init__(self, file, encoding="utf-8"):  # noqa: D107
        # type: (Union[str, BinaryIO], str) -> None
        super().__init__()
        self._file = file
        self.encoding = encoding
        if isinstance(file, (str, bytes)):
            self._tar = tarfile.open(file, mode="r")
        else:
            self._tar = tarfile.open(fileobj=file, mode="r")

        self._directory_cache = None

    @property
    def _directory_entries(self):
        """Lazy directory cache."""
        if self._directory_cache is None:
            _decode = self._decode
            _directory_entries = (
                (_decode(info.name).strip("/"), info) for info in self._tar
            )

            def _list_tar():
                for name, info in _directory_entries:
                    try:
                        _name = normpath(name)
                    except IllegalBackReference:
                        # Back references outside root, must be up to no good.
                        pass
                    else:
                        if _name:
                            yield _name, info

            self._directory_cache = OrderedDict(_list_tar())
        return self._directory_cache

    def __repr__(self):
        # type: () -> str
        return "ReadTarFS({!r})".format(self._file)

    def __str__(self):
        # type: () -> str
        return "<TarFS '{}'>".format(self._file)

    def _encode(self, s):
        # type: (str) -> str
        return s

    def _decode(self, s):
        # type: (str) -> str
        return s

    def getinfo(self, path, namespaces=None):
        # type: (str, Optional[Collection[str]]) -> Info
        _path = relpath(self.validatepath(path))
        namespaces = namespaces or ()
        raw_info = {}  # type: dict[str, dict[str, object]]

        if not _path:
            raw_info["basic"] = {"name": "", "is_dir": True}
            if "details" in namespaces:
                raw_info["details"] = {"type": int(ResourceType.directory)}

        else:
            try:
                implicit = False
                member = self._directory_entries[_path]
            except KeyError:
                if not self.isdir(_path):
                    raise errors.ResourceNotFound(path)
                implicit = True
                member = tarfile.TarInfo(_path)
                member.type = tarfile.DIRTYPE

            raw_info["basic"] = {
                "name": basename(self._decode(member.name)),
                "is_dir": member.isdir(),
            }

            if "details" in namespaces:
                raw_info["details"] = {
                    "size": member.size,
                    "type": int(self.type_map[member.type]),
                }
                if not implicit:
                    raw_info["details"]["modified"] = member.mtime
            if "access" in namespaces and not implicit:
                raw_info["access"] = {
                    "gid": member.gid,
                    "group": member.gname,
                    "permissions": Permissions(mode=member.mode).dump(),
                    "uid": member.uid,
                    "user": member.uname,
                }
            if "tar" in namespaces and not implicit:
                raw_info["tar"] = _get_member_info(member, self.encoding)
                raw_info["tar"].update(
                    {
                        k.replace("is", "is_"): getattr(member, k)()
                        for k in dir(member)
                        if k.startswith("is")
                    }
                )

        return Info(raw_info)

    def isdir(self, path):
        _path = relpath(self.validatepath(path))
        try:
            return self._directory_entries[_path].isdir()
        except KeyError:
            return any(isbase(_path, name) for name in self._directory_entries)

    def isfile(self, path):
        _path = relpath(self.validatepath(path))
        try:
            return self._directory_entries[_path].isfile()
        except KeyError:
            return False

    def setinfo(self, path, info):
        # type: (str, RawInfo) -> None
        self.check()
        raise errors.ResourceReadOnly(path)

    def listdir(self, path):
        # type: (str) -> list[str]
        _path = relpath(self.validatepath(path))

        if not self.gettype(path) is ResourceType.directory:
            raise errors.DirectoryExpected(path)

        children = (
            frombase(_path, n) for n in self._directory_entries if isbase(_path, n)
        )
        content = (parts(child)[1] for child in children if relpath(child))
        return list(OrderedDict.fromkeys(content))

    def makedir(
        self,  # type: T
        path,  # type: str
        permissions=None,  # type: Optional[Permissions]
        recreate=False,  # type: bool
    ):
        # type: (...) -> SubFS[T]
        self.check()
        raise errors.ResourceReadOnly(path)

    def openbin(self, path, mode="r", buffering=-1, **options):
        # type: (str, str, int, **Any) -> BinaryIO
        _path = relpath(self.validatepath(path))

        if "w" in mode or "+" in mode or "a" in mode:
            raise errors.ResourceReadOnly(path)

        try:
            member = self._directory_entries[_path]
        except KeyError:
            raise errors.ResourceNotFound(path)

        if not member.isfile():
            raise errors.FileExpected(path)

        rw = RawWrapper(cast(IO, self._tar.extractfile(member)))
        return rw  # type: ignore

    def remove(self, path):
        # type: (str) -> None
        self.check()
        raise errors.ResourceReadOnly(path)

    def removedir(self, path):
        # type: (str) -> None
        self.check()
        raise errors.ResourceReadOnly(path)

    def close(self):
        # type: () -> None
        super().close()
        if hasattr(self, "_tar"):
            self._tar.close()

    def isclosed(self):
        # type: () -> bool
        return self._tar.closed  # type: ignore

    def geturl(self, path, purpose="download"):
        # type: (str, str) -> str
        if purpose == "fs" and isinstance(self._file, str):
            quoted_file = url_quote(self._file)
            quoted_path = url_quote(path)
            return "tar://{}!/{}".format(quoted_file, quoted_path)
        else:
            raise NoURL(path, purpose)


if __name__ == "__main__":  # pragma: no cover
    from fs3.tree import render

    with TarFS("tests.tar") as tar_fs:
        print(tar_fs.listdir("/"))
        print(tar_fs.listdir("/tests/"))
        print(tar_fs.readtext("tests/ttt/settings.ini"))
        render(tar_fs)
        print(tar_fs)
        print(repr(tar_fs))

    with TarFS("TarFS.tar", write=True) as tar_fs:
        tar_fs.makedirs("foo/bar")
        tar_fs.writetext("foo/bar/baz.txt", "Hello, World")
        print(tar_fs)
        print(repr(tar_fs))
