import sys

import unittest


class TestImports(unittest.TestCase):
    def test_import_path(self):
        """Test import fs3 also imports other symbols."""
        restore_fs = sys.modules.pop("fs3")
        sys.modules.pop("fs3.path")
        try:
            import fs3

            fs3.path
            fs3.Seek
            fs3.ResourceType
            fs3.open_fs
        finally:
            sys.modules["fs3"] = restore_fs
