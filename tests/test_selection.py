import sublime
import sys
import os

from . import unittest
from LaravelGoto.lib.selection import Selection


class TestSelection(unittest.ViewTestCase):
    def test_hello_world(self):
        self.fixture("""
            'hello_|world'
        """)

        selection = Selection(self.view)

        self.assertEqual('hello_world', selection.get_path())

    def test_blade_comment(self):
        self.fixture("""
            '{{-- resources/views/comp|onents/layout --}}'
        """)

        selection = Selection(self.view)

        self.assertEqual('resources/views/components/layout', selection.get_path())


