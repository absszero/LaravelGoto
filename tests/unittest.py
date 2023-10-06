import os
from unittest import TestCase
from unittest import mock  # noqa: F401
from unittest import skipIf  # noqa: F401

from os import path
from sublime import find_resources
from sublime import active_window


class ViewTestCase(TestCase):

    def setUp(self):
        self.view = active_window().create_output_panel(
            'test_view',
            unlisted=True
        )
        self.view.set_scratch(True)
        self.view.settings().set('auto_indent', False)
        self.view.settings().set('indent_to_bracket', False)
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('trim_automatic_white_space', False)
        self.view.settings().set('smart_indent', True)
        self.view.settings().set('tab_size', 4)
        self.view.settings().set('translate_tabs_to_spaces', True)
        self.view.set_syntax_file(find_resources('PHP.sublime-syntax')[0])

    def tearDown(self):
        if self.view:
            self.view.close()

    def fixture(self, text):
        self.view.run_command('setup_fixture', {'text': '<?php ' + text})

    def get_test_dir(self):
        return path.dirname(path.abspath(__file__))

    def get_http_kernel(self):
        test_dir = self.get_test_dir()
        fullpath = path.join(test_dir, 'fixtures/app/Http/Kernel.php')
        with open(fullpath, mode = "r", encoding = "utf-8") as f:
            return f.read()

