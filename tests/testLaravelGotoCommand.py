import sublime
import sys
import os
from unittest import TestCase


class TestLaravelGotoCommand(TestCase):
    @classmethod
    def setUpClass(self):
        self.window = sublime.active_window()
        sample = os.path.dirname(__file__) + '/sample.php'
        self.view = self.window.open_file(sample)
        while self.view.is_loading():
            pass
        # make sure we have a window to work with
        s = sublime.load_settings("Preferences.sublime-settings")
        s.set("close_windows_when_empty", False)

    @classmethod
    def tearDownClass(self):
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
        self.assert_select(35, 'HelloController.php@index')

    def test_view(self):
        self.assert_select(100, 'hello_view.blade.php')

    def test_staticFile(self):
        self.assert_select(118, 'hello.JS')

    def test_namespace58(self):
        self.assert_select(200, '58\\FiveEightController.php@index')

    def test_namespace52(self):
        self.assert_select(300, '52\\FiveTwoController.php@index')

    def test_namespaceLumen(self):
        self.assert_select(420, 'Lumen\\LumenController.php@index')

    def test_view_namespace(self):
        self.assert_select(500, 'hello_view.blade.php')

    def test_css(self):
        self.assert_select(530, 'hello.css')

    def test_absolute_path(self):
        self.assert_select(630, '\\Absolute\\IndexController.php@index')

    def test_facade_config_get(self):
        self.assert_select(685, 'config/app.php')

    def test_facade_config_set(self):
        self.assert_select(720, 'config/app.php')

    def test_config_get_only_file(self):
        self.assert_select(747, 'config/app.php')

    def test_config_get(self):
        self.assert_select(765, 'config/app.php')

    def test_config_set(self):
        self.assert_select(800, 'config/app.php')

    def test_config_in_config(self):
        self.assert_select(1055, 'config/app.php')

    def test_env(self):
        self.assert_select(830, '.env')

    def test_lang_underscore(self):
        self.assert_select(860, 'resources/lang/messages.php')

    def test_lang_blade_directive(self):
        self.assert_select(890, 'resources/lang/messages.php')

    def test_lang_trans(self):
        self.assert_select(920, 'resources/lang/messages.php')

    def test_lang_trans_choice(self):
        self.assert_select(950, 'resources/lang/messages.php')

    def test_lang_trans_package(self):
        self.assert_select(985, 'resources/lang/vendor/package/messages.php')

    def test_relative_path_static_file(self):
        self.assert_select(1005, 'hello.css')

    def test_package_view(self):
        self.assert_select(1080, 'package/hello_view.blade.php')

    def test_app_path(self):
        self.assert_select(1110, 'app/User.php')

    def test_config_path(self):
        self.assert_select(1155, 'config/app.php')

    def test_database_path(self):
        self.assert_select(1185, 'database/UserFactory.php')

    def test_public_path(self):
        self.assert_select(1220, 'public/css/app.css')

    def test_resource_path(self):
        self.assert_select(1250, 'resources/sass/app.scss')

    def test_storage_path(self):
        self.assert_select(1285, 'storage/logs/laravel.log')

    def test_double_brackets_path(self):
        self.assert_select(1330, 'storage/logs/laravel.log')

    def test_v8_namespace_route(self):
        self.assert_select(1365, 'L8\\EightController.php@index')

    def test_v8_route(self):
        self.assert_select(1420, 'EightController.php')

    def test_v8_group_namespae_route(self):
        self.assert_select(1520, 'L8\\EightController.php@index')

    def assert_select(self, point, expectation):
        sel = self.view.sel()
        sel.clear()
        sel.add(sublime.Region(point, point))
        self.view.run_command("laravel_goto")
        self.window.run_command("select_all")
        self.window.run_command("copy")
        text = sublime.get_clipboard()
        self.window.run_command("hide_overlay")
        self.assertEqual(text, expectation)
