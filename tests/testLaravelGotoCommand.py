import sublime
import sys
import os
from unittest import TestCase


class TestLaravelGotoCommand(TestCase):
    def setUp(self):
        self.window = sublime.active_window()
        sample = os.path.dirname(__file__) + '/sample.php'
        self.view = self.window.open_file(sample)
        while self.view.is_loading():
            pass
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    def tearDown(self):
        if (self.window.active_view() != self.view):
            try:
                self.window.active_view().window().run_command("close_file")
            except Exception as e:
                pass

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

    def test_absolute_path(self):
        self.assert_select(630, 'IndexController.php')

    def test_facade_config_get(self):
        self.assert_select(685, 'app.php')

    def test_facade_config_set(self):
        self.assert_select(720, 'app.php')

    def test_config_get_only_file(self):
        self.assert_select(747, 'app.php')

    def test_config_get(self):
        self.assert_select(765, 'app.php')

    def test_config_set(self):
        self.assert_select(800, 'app.php')

    def test_config_in_config(self):
        self.assert_select(1055, 'app.php')

    def test_env(self):
        self.assert_select(830, '.env')

    def test_lang_underscore(self):
        self.assert_select(860, 'messages.php')

    def test_lang_blade_directive(self):
        self.assert_select(890, 'messages.php')

    def test_lang_trans(self):
        self.assert_select(920, 'messages.php')

    def test_lang_trans_choice(self):
        self.assert_select(950, 'messages.php')

    def test_lang_trans_package(self):
        self.assert_select(985, 'messages.php')

    def test_relative_path_static_file(self):
        self.assert_select(1005, 'hello.css')

    def test_package_view(self):
        self.assert_select(1080, 'hello_view.blade.php')

    def assert_select(self, point, expectation):
        sel = self.view.sel()
        sel.clear()
        sel.add(sublime.Region(point, point))
        self.view.run_command("laravel_goto")
        filename = self.window.active_view().file_name()
        self.assertEqual(os.path.basename(filename), expectation)
