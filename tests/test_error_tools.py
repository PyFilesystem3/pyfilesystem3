import errno
import unittest

import fs3.errors
from fs3.error_tools import convert_os_errors


class TestErrorTools(unittest.TestCase):
    def test_convert_enoent(self):
        exception = OSError(errno.ENOENT, "resource not found")
        with self.assertRaises(fs3.errors.ResourceNotFound) as ctx:
            with convert_os_errors("stat", "/tmp/test"):
                raise exception
        self.assertEqual(ctx.exception.exc, exception)
        self.assertEqual(ctx.exception.path, "/tmp/test")

    def test_convert_enametoolong(self):
        exception = OSError(errno.ENAMETOOLONG, "File name too long: test")
        with self.assertRaises(fs3.errors.PathError) as ctx:
            with convert_os_errors("stat", "/tmp/test"):
                raise exception
        self.assertEqual(ctx.exception.exc, exception)
        self.assertEqual(ctx.exception.path, "/tmp/test")
