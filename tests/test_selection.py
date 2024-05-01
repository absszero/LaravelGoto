from . import unittest
from LaravelGoto.lib.selection import Selection


class TestSelection(unittest.ViewTestCase):
    def test_var(self):
        self.fixture("""
            'ap|p.{$var}.timezone'
            """)

        selection = Selection(self.view)
        self.assertEqual('app', selection.get_path())

        self.fixture("""
            "ap|p.$var.timezone"
            """)

        # cursor on a php $var
        selection = Selection(self.view)
        self.assertEqual('app', selection.get_path())

        self.fixture("""
            "app.$v|ar.timezone"
            """)

        selection = Selection(self.view)
        self.assertEqual('app', selection.get_path())

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

        self.assertEqual(
            'resources/views/components/layout',
            selection.get_path()
            )

    def test_get_lines_after_delimiter(self):
        self.fixture("""
view(
    'hell|o_view',
    ['name' => 'James']
);
        """)

        selection = Selection(self.view)
        lines = selection.get_lines_after_delimiter()
        self.assertEqual("view('hello_view',", lines)
