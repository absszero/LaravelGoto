import sublime
import sys
import os

from . import unittest
from LaravelGoto.lib.workspace import get_file_content


class TestWorkspace(unittest.ViewTestCase):
    def test_get_file_content(self):
        folder = os.path.dirname(os.path.abspath(__file__));
        content = get_file_content(folder, 'Http/Kernel.php')
        self.assertTrue(content.__contains__('class Kernel extends HttpKernel'))
