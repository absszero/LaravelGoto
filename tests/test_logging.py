from . import unittest
from LaravelGoto.lib.logging import Logging


class TestLogging(unittest.ViewTestCase):
    logging = Logging()

    def test_channel(self):
        place = self.logging.get_place(
            'slack', "Log::channel('slack')",
        )
        self.assertEqual("config/logging.php", place.path)
        self.assertEqual('([\'"]{1})slack\\1\\s*=>', place.location)

    def test_stack(self):
        place = self.logging.get_place(
            'slack', "Log::stack(['slack', 'single'])",
        )
        self.assertEqual("config/logging.php", place.path)
        self.assertEqual('([\'"]{1})slack\\1\\s*=>', place.location)

        place = self.logging.get_place(
            'single', "Log::stack(['slack', 'single'])",
        )
        self.assertEqual('([\'"]{1})single\\1\\s*=>', place.location)
