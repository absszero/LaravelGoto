from . import unittest
from LaravelGoto.lib.config import Config


class TestConfig(unittest.ViewTestCase):
    config = Config()

    def test_php_var(self):
        place = self.config.get_place(
            'app',
            """Config::get('app.{$var}');"""
            )
        self.assertEqual('config/app.php', place.path)

    def test_facade_config_get(self):
        place = self.config.get_place(
            'app.timezone',
            """Config::get('app.timezone');"""
            )
        self.assertEqual('config/app.php', place.path)
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_facade_config_set(self):
        place = self.config.get_place(
            'app',
            """Config::set(   'app', 'UTC');"""
            )
        self.assertEqual('config/app.php', place.path)

    def test_config_get_only_file(self):
        place = self.config.get_place(
            'app',
            """config('app');"""
            )
        self.assertEqual('config/app.php', place.path)

    def test_config_get_helper(self):
        place = self.config.get_place(
            'app.timezone',
            """config('app.timezone');"""
            )
        self.assertEqual('config/app.php', place.path)
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_config_set_helper(self):
        place = self.config.get_place(
            'app',
            """config(     ['app' => 'UTC']);"""
            )
        self.assertEqual('config/app.php', place.path)

    def test_not_in_path(self):
        place = self.config.get_place(
            'Foo',
            """Foo::get(config(     ['app' => 'UTC']);)"""
            )
        self.assertFalse(place)

    def test_multiline(self):
        place = self.config.get_place(
            'app.timezone',
            "'app.timezone' => 'UTC']",
            """config(     [
                'app.timezone' => 'UTC']
            );"""
        )
        self.assertEqual('config/app.php', place.path)
