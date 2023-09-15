import sublime
import sys
import os

from . import unittest
from LaravelGoto.lib.workspace import get_path, get_file_content


class TestWorkspace(unittest.ViewTestCase):
    def test_get_file_content(self):
        folder = os.path.dirname(os.path.abspath(__file__));
        content = get_file_content(folder, 'app/Http/Kernel.php')
        self.assertTrue(content.__contains__('class Kernel extends HttpKernel'))

    def test_get_path(self):
        folder = os.path.dirname(os.path.abspath(__file__));
        fullpapth = get_path(folder, 'app/Http/Kernel.php', True)
        self.assertTrue(fullpapth.__contains__('app/Http/Kernel.php'))

