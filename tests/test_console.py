import sublime
import sys
import os

from unittest.mock import patch
from . import unittest
from LaravelGoto.lib.console import Console


class TestConsole(unittest.ViewTestCase):
    @patch('LaravelGoto.lib.workspace.get_folders')
    def test_all(self, mock_get_folders):
        mock_get_folders.return_value = [self.get_test_dir()]

        console = Console()
        commands = console.all()

        self.assertEqual(commands.get("app:say-hello").path, 'SayHello.php');
        self.assertEqual(commands.get("app:send-mails").path, 'SendEmails.php');
        self.assertEqual(commands.get("app:say-goodbye").path, 'app/Console/Commands/SayGoodbye.php');

