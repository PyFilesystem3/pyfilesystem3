import shutil
import tempfile
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

import fs3.test
from fs3 import appfs


class _TestAppFS(fs3.test.FSTestCases):

    AppFS = None

    @classmethod
    def setUpClass(cls):
        super(_TestAppFS, cls).setUpClass()
        cls.tmpdir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmpdir)

    def make_fs(self):
        with mock.patch(
            "appdirs.{}".format(self.AppFS.app_dir),
            autospec=True,
            spec_set=True,
            return_value=tempfile.mkdtemp(dir=self.tmpdir),
        ):
            return self.AppFS("fstest", "willmcgugan", "1.0")

    def test_repr(self):
        self.assertEqual(
            repr(self.fs),
            "{}('fstest', author='willmcgugan', version='1.0')".format(
                self.AppFS.__name__
            ),
        )

    def test_str(self):
        self.assertEqual(
            str(self.fs), "<{} 'fstest'>".format(self.AppFS.__name__.lower())
        )


class TestUserDataFS(_TestAppFS, unittest.TestCase):
    AppFS = appfs.UserDataFS


class TestUserConfigFS(_TestAppFS, unittest.TestCase):
    AppFS = appfs.UserConfigFS


class TestUserCacheFS(_TestAppFS, unittest.TestCase):
    AppFS = appfs.UserCacheFS


class TestSiteDataFS(_TestAppFS, unittest.TestCase):
    AppFS = appfs.SiteDataFS


class TestSiteConfigFS(_TestAppFS, unittest.TestCase):
    AppFS = appfs.SiteConfigFS


class TestUserLogFS(_TestAppFS, unittest.TestCase):
    AppFS = appfs.UserLogFS
