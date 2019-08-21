import sublime
import sys
import os
from unittest import TestCase


class TestLaravelGotoCommand(TestCase):
    def setUp(self):
        self.window = sublime.active_window()
        route = os.path.dirname(__file__) + '/route.php'
        self.view = self.window.open_file(route)
        while self.view.is_loading():
            pass
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def test_controller(self):
        self.select(35)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name()
        self.assertEqual(os.path.basename(file_name), "HelloController.php")

    def test_view(self):
        self.select(100)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name()
        self.assertEqual(os.path.basename(file_name), "hello_view.blade.php")

    def test_staticFile(self):
        self.select(118)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name()
        self.assertEqual(os.path.basename(file_name), "hello.js")

    def test_namespace58(self):
        self.select(200)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name()
        self.assertEqual(
            os.path.basename(file_name),
            "FiveEightController.php"
        )

    def test_namespace52(self):
        self.select(300)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name()
        self.assertEqual(
            os.path.basename(file_name),
            "FiveTwoController.php"
        )

    def test_namespaceLumen(self):
        self.select(420)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name()
        self.assertEqual(
            os.path.basename(file_name),
            "LumenController.php"
        )

    # select a place
    def select(self, point):
        sel = self.view.sel()
        sel.clear()
        sel.add(sublime.Region(point, point))
