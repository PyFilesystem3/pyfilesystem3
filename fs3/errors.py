"""Exception classes thrown by filesystem operations.

Errors relating to the underlying filesystem are translated in
to one of the following exceptions.

All Exception classes are derived from `~fs3.errors.FSError`
which may be used as a catch-all filesystem exception.

"""

import typing

import functools

if typing.TYPE_CHECKING:
    from typing import Optional


__all__ = [
    "BulkCopyFailed",
    "CreateFailed",
    "DestinationExists",
    "DirectoryExists",
    "DirectoryExpected",
    "DirectoryNotEmpty",
    "FileExists",
    "FileExpected",
    "FilesystemClosed",
    "FSError",
    "IllegalBackReference",
    "IllegalDestination",
    "InsufficientStorage",
    "InvalidCharsInPath",
    "InvalidPath",
    "MissingInfoNamespace",
    "NoSysPath",
    "NoURL",
    "OperationFailed",
    "OperationTimeout",
    "PathError",
    "PatternError",
    "PermissionDenied",
    "RemoteConnectionError",
    "RemoveRootError",
    "ResourceError",
    "ResourceInvalid",
    "ResourceLocked",
    "ResourceNotFound",
    "ResourceReadOnly",
    "Unsupported",
    "UnsupportedHash",
]


class MissingInfoNamespace(AttributeError):
    """An expected namespace is missing."""

    def __init__(self, namespace):  # noqa: D107
        # type: (str) -> None
        self.namespace = namespace
        msg = "namespace '{}' is required for this attribute"
        super().__init__(msg.format(namespace))

    def __reduce__(self):
        return type(self), (self.namespace,)


class FSError(Exception):
    """Base exception for the `fs3` module."""

    default_message = "Unspecified error"

    def __init__(self, msg=None):  # noqa: D107
        # type: (Optional[str]) -> None
        self._msg = msg or self.default_message
        super().__init__()

    def __str__(self):
        # type: () -> str
        """Return the error message."""
        msg = self._msg.format(**self.__dict__)
        return msg

    def __repr__(self):
        # type: () -> str
        msg = self._msg.format(**self.__dict__)
        return "{}({!r})".format(self.__class__.__name__, msg)


class FilesystemClosed(FSError):
    """Attempt to use a closed filesystem."""

    default_message = "attempt to use closed filesystem"


class BulkCopyFailed(FSError):
    """A copy operation failed in worker threads."""

    default_message = "One or more copy operations failed (see errors attribute)"

    def __init__(self, errors):  # noqa: D107
        self.errors = errors
        super().__init__()


class CreateFailed(FSError):
    """Filesystem could not be created."""

    default_message = "unable to create filesystem, {details}"

    def __init__(self, msg=None, exc=None):  # noqa: D107
        # type: (Optional[str], Optional[Exception]) -> None
        self._msg = msg or self.default_message
        self.details = "" if exc is None else str(exc)
        self.exc = exc

    @classmethod
    def catch_all(cls, func):
        @functools.wraps(func)
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except cls:
                raise
            except Exception as e:
                raise cls(exc=e)

        return new_func  # type: ignore

    def __reduce__(self):
        return type(self), (self._msg, self.exc)


class PathError(FSError):
    """Base exception for errors to do with a path string."""

    default_message = "path '{path}' is invalid"

    def __init__(self, path, msg=None, exc=None):  # noqa: D107
        # type: (str, Optional[str], Optional[Exception]) -> None
        self.path = path
        self.exc = exc
        super().__init__(msg=msg)

    def __reduce__(self):
        return type(self), (self.path, self._msg, self.exc)


class NoSysPath(PathError):
    """The filesystem does not provide *sys paths* to the resource."""

    default_message = "path '{path}' does not map to the local filesystem"


class NoURL(PathError):
    """The filesystem does not provide an URL for the resource."""

    default_message = "path '{path}' has no '{purpose}' URL"

    def __init__(self, path, purpose, msg=None):  # noqa: D107
        # type: (str, str, Optional[str]) -> None
        self.purpose = purpose
        super().__init__(path, msg=msg)

    def __reduce__(self):
        return type(self), (self.path, self.purpose, self._msg)


class InvalidPath(PathError):
    """Path can't be mapped on to the underlaying filesystem."""

    default_message = "path '{path}' is invalid on this filesystem "


class InvalidCharsInPath(InvalidPath):
    """Path contains characters that are invalid on this filesystem."""

    default_message = "path '{path}' contains invalid characters"


class OperationFailed(FSError):
    """A specific operation failed."""

    default_message = "operation failed, {details}"

    def __init__(
        self,
        path=None,  # type: Optional[str]
        exc=None,  # type: Optional[Exception]
        msg=None,  # type: Optional[str]
    ):  # noqa: D107
        # type: (...) -> None
        self.path = path
        self.exc = exc
        self.details = "" if exc is None else str(exc)
        self.errno = getattr(exc, "errno", None)
        super().__init__(msg=msg)

    def __reduce__(self):
        return type(self), (self.path, self.exc, self._msg)


class Unsupported(OperationFailed):
    """Operation not supported by the filesystem."""

    default_message = "not supported"


class RemoteConnectionError(OperationFailed):
    """Operations encountered remote connection trouble."""

    default_message = "remote connection error"


class InsufficientStorage(OperationFailed):
    """Storage is insufficient for requested operation."""

    default_message = "insufficient storage space"


class PermissionDenied(OperationFailed):
    """Not enough permissions."""

    default_message = "permission denied"


class OperationTimeout(OperationFailed):
    """Filesystem took too long."""

    default_message = "operation timed out"


class RemoveRootError(OperationFailed):
    """Attempt to remove the root directory."""

    default_message = "root directory may not be removed"


class IllegalDestination(OperationFailed):
    """The given destination cannot be used for the operation.

    This error will occur when attempting to move / copy a folder into itself or copying
    a file onto itself.
    """

    default_message = "'{path}' is not a legal destination"


class ResourceError(FSError):
    """Base exception class for error associated with a specific resource."""

    default_message = "failed on path {path}"

    def __init__(self, path, exc=None, msg=None):  # noqa: D107
        # type: (str, Optional[Exception], Optional[str]) -> None
        self.path = path
        self.exc = exc
        super().__init__(msg=msg)

    def __reduce__(self):
        return type(self), (self.path, self.exc, self._msg)


class ResourceNotFound(ResourceError):
    """Required resource not found."""

    default_message = "resource '{path}' not found"


class ResourceInvalid(ResourceError):
    """Resource has the wrong type."""

    default_message = "resource '{path}' is invalid for this operation"


class FileExists(ResourceError):
    """File already exists."""

    default_message = "resource '{path}' exists"


class FileExpected(ResourceInvalid):
    """Operation only works on files."""

    default_message = "path '{path}' should be a file"


class DirectoryExpected(ResourceInvalid):
    """Operation only works on directories."""

    default_message = "path '{path}' should be a directory"


class DestinationExists(ResourceError):
    """Target destination already exists."""

    default_message = "destination '{path}' exists"


class DirectoryExists(ResourceError):
    """Directory already exists."""

    default_message = "directory '{path}' exists"


class DirectoryNotEmpty(ResourceError):
    """Attempt to remove a non-empty directory."""

    default_message = "directory '{path}' is not empty"


class ResourceLocked(ResourceError):
    """Attempt to use a locked resource."""

    default_message = "resource '{path}' is locked"


class ResourceReadOnly(ResourceError):
    """Attempting to modify a read-only resource."""

    default_message = "resource '{path}' is read only"


class IllegalBackReference(ValueError):
    """Too many backrefs exist in a path.

    This error will occur if the back references in a path would be
    outside of the root. For example, ``"/foo/../../"``, contains two back
    references which would reference a directory above the root.

    Note:
        This exception is a subclass of `ValueError` as it is not
        strictly speaking an issue with a filesystem or resource.

    """

    def __init__(self, path):  # noqa: D107
        # type: (str) -> None
        self.path = path
        msg = ("path '{path}' contains back-references outside of filesystem").format(
            path=path
        )
        super().__init__(msg)

    def __reduce__(self):
        return type(self), (self.path,)


class UnsupportedHash(ValueError):
    """The requested hash algorithm is not supported.

    This exception will be thrown if a hash algorithm is requested that is
    not supported by hashlib.

    """


class PatternError(ValueError):
    """A string pattern with invalid syntax was given."""

    default_message = "pattern '{pattern}' is invalid at position {position}"

    def __init__(self, pattern, position, exc=None, msg=None):  # noqa: D107
        # type: (str, int, Optional[Exception], Optional[str]) -> None
        self.pattern = pattern
        self.position = position
        self.exc = exc
        super().__init__()

    def __reduce__(self):
        return type(self), (self.path, self.position, self.exc, self._msg)
