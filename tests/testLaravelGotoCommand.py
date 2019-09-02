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
        self.assert_select(35, 'HelloController.php')

    def test_view(self):
        self.assert_select(100, 'hello_view.blade.php')

    def test_staticFile(self):
        self.assert_select(118, 'hello.js')

    def test_namespace58(self):
        self.assert_select(200, 'FiveEightController.php')

    def test_namespace52(self):
        self.assert_select(300, 'FiveTwoController.php')

    def test_namespaceLumen(self):
        self.assert_select(420, 'LumenController.php')

    def test_view_namespace(self):
        self.assert_select(500, 'hello_view.blade.php')

    def test_css(self):
        self.assert_select(530, 'hello.css')

    # select a place
    def assert_select(self, point, expectation):
        sel = self.view.sel()
        sel.clear()
        sel.add(sublime.Region(point, point))
        self.view.run_command("laravel_goto")
        filename = self.window.active_view().file_name()
        self.assertEqual(os.path.basename(filename), expectation)
