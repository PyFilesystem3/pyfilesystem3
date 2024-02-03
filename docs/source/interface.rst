.. _interface:

PyFilesystem3 API
-----------------

The following is a complete list of methods on PyFilesystem3 objects.

* :meth:`~fs3.base.FS.appendbytes` Append bytes to a file.
* :meth:`~fs3.base.FS.appendtext` Append text to a file.
* :meth:`~fs3.base.FS.check` Check if a filesystem is open or raise error.
* :meth:`~fs3.base.FS.close` Close the filesystem.
* :meth:`~fs3.base.FS.copy` Copy a file to another location.
* :meth:`~fs3.base.FS.copydir` Copy a directory to another location.
* :meth:`~fs3.base.FS.create` Create or truncate a file.
* :meth:`~fs3.base.FS.desc` Get a description of a resource.
* :meth:`~fs3.base.FS.download` Copy a file on the filesystem to a file-like object.
* :meth:`~fs3.base.FS.exists` Check if a path exists.
* :meth:`~fs3.base.FS.filterdir` Iterate resources, filtering by wildcard(s).
* :meth:`~fs3.base.FS.getbasic` Get basic info namespace for a resource.
* :meth:`~fs3.base.FS.getdetails` Get details info namespace for a resource.
* :meth:`~fs3.base.FS.getinfo` Get info regarding a file or directory.
* :meth:`~fs3.base.FS.getmeta` Get meta information for a resource.
* :meth:`~fs3.base.FS.getmodified` Get the last modified time of a resource.
* :meth:`~fs3.base.FS.getospath` Get path with encoding expected by the OS.
* :meth:`~fs3.base.FS.getsize` Get the size of a file.
* :meth:`~fs3.base.FS.getsyspath` Get the system path of a resource, if one exists.
* :meth:`~fs3.base.FS.gettype` Get the type of a resource.
* :meth:`~fs3.base.FS.geturl` Get a URL to a resource, if one exists.
* :meth:`~fs3.base.FS.hassyspath` Check if a resource maps to the OS filesystem.
* :meth:`~fs3.base.FS.hash` Get the hash of a file's contents.
* :meth:`~fs3.base.FS.hasurl` Check if a resource has a URL.
* :meth:`~fs3.base.FS.isclosed` Check if the filesystem is closed.
* :meth:`~fs3.base.FS.isempty` Check if a directory is empty.
* :meth:`~fs3.base.FS.isdir` Check if path maps to a directory.
* :meth:`~fs3.base.FS.isfile` Check if path maps to a file.
* :meth:`~fs3.base.FS.islink` Check if path is a link.
* :meth:`~fs3.base.FS.listdir` Get a list of resources in a directory.
* :meth:`~fs3.base.FS.lock` Get a thread lock context manager.
* :meth:`~fs3.base.FS.makedir` Make a directory.
* :meth:`~fs3.base.FS.makedirs` Make a directory and intermediate directories.
* :meth:`~fs3.base.FS.match` Match one or more wildcard patterns against a path.
* :meth:`~fs3.base.FS.move` Move a file to another location.
* :meth:`~fs3.base.FS.movedir` Move a directory to another location.
* :meth:`~fs3.base.FS.open` Open a file on the filesystem.
* :meth:`~fs3.base.FS.openbin` Open a binary file.
* :meth:`~fs3.base.FS.opendir` Get a filesystem object for a directory.
* :meth:`~fs3.base.FS.readbytes` Read file as bytes.
* :meth:`~fs3.base.FS.readtext` Read file as text.
* :meth:`~fs3.base.FS.remove` Remove a file.
* :meth:`~fs3.base.FS.removedir` Remove a directory.
* :meth:`~fs3.base.FS.removetree` Recursively remove file and directories.
* :meth:`~fs3.base.FS.scandir` Scan files and directories.
* :meth:`~fs3.base.FS.setinfo` Set resource information.
* :meth:`~fs3.base.FS.settimes` Set modified times for a resource.
* :meth:`~fs3.base.FS.touch` Create a file or update times.
* :meth:`~fs3.base.FS.tree` Render a tree view of the filesystem.
* :meth:`~fs3.base.FS.upload` Copy a binary file to the filesystem.
* :meth:`~fs3.base.FS.validatepath` Check a path is valid and return normalized path.
* :meth:`~fs3.base.FS.writebytes` Write a file as bytes.
* :meth:`~fs3.base.FS.writefile` Write a file-like object to the filesystem.
* :meth:`~fs3.base.FS.writetext` Write a file as text.
