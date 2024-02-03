import unittest
from datetime import datetime, timezone

from fs3.time import datetime_to_epoch, epoch_to_datetime


class TestEpoch(unittest.TestCase):
    def test_epoch_to_datetime(self):
        self.assertEqual(
            epoch_to_datetime(142214400), datetime(1974, 7, 5, tzinfo=timezone.utc)
        )

    def test_datetime_to_epoch(self):
        self.assertEqual(
            datetime_to_epoch(datetime(1974, 7, 5, tzinfo=timezone.utc)), 142214400
        )
