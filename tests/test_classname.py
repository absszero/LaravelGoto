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

    def test_backslash(self):
        place = self.classname.get_place(
            'Livewire/Admin/Elevator/Elevator',
            """Livewire/Admin/Elevator/Elevator"""
            )
        self.assertEqual('Livewire/Admin/Elevator/Elevator.php', place.path)
