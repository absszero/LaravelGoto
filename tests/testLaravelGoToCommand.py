import sublime
import sys
import os
from pprint import pprint
from unittest import TestCase

class TestLaravelGotoCommand(TestCase):
    def setUp(self):
        route = os.path.dirname(__file__) + '/route.php'
        self.window = sublime.active_window()
        self.view = self.window.open_file(route)
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def testController(self):
        r = sublime.Region(35, 35)
        while self.view.is_loading():
            pass
        sel = self.view.sel()
        sel.clear()
        sel.add(r)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name();
        self.assertEqual(os.path.basename(file_name), "HelloController.php")

    def testView(self):
        r = sublime.Region(100, 100)
        while self.view.is_loading():
            pass
        sel = self.view.sel()
        sel.clear()
        sel.add(r)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name();
        self.assertEqual(os.path.basename(file_name), "hello_view.blade.php")

    def testStaticFile(self):
        r = sublime.Region(119, 119)
        while self.view.is_loading():
            pass
        sel = self.view.sel()
        sel.clear()
        sel.add(r)
        self.view.run_command("laravel_goto")
        file_name = self.window.active_view().file_name();
        self.assertEqual(os.path.basename(file_name), "hello.js")
