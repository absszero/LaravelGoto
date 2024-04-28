from . import unittest
from LaravelGoto.lib.classname import ClassName


class TestClassName(unittest.ViewTestCase):
    classname = ClassName()

    def test_php_var(self):
        place = self.classname.get_place(
            'App\\Models\\Score',
            """return $this->hasMany('App\\Mod|els\\Score');"""
            )
        self.assertEqual('App\\Models\\Score.php', place.path)
