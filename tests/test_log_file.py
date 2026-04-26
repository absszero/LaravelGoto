import os
from unittest.mock import patch
from . import unittest
from LaravelGoto.lib.log_file import LogFile


FIXTURE_CONFIG = """<?php

return [
    'channels' => [
        'sentry_logs' => [
            'driver' => 'sentry_logs',
            'level' => env('LOG_LEVEL', 'debug'),
        ],

        'single' => [
            'driver' => 'single',
            'path' => storage_path('logs/laravel.log'),
            'level' => env('LOG_LEVEL', 'debug'),
        ],

        'daily' => [
            'driver' => 'daily',
            'path' => storage_path('logs/laravelDaily/laravel.log'),
            'level' => env('LOG_LEVEL', 'debug'),
        ],
    ],
];
"""


class TestLogFile(unittest.ViewTestCase):

    def test_channels_returns_channels_with_path(self):
        log_file = LogFile(logging_config=FIXTURE_CONFIG)
        channels = log_file.channels()

        self.assertIn('single', channels)
        self.assertEqual(channels['single'], "storage_path('logs/laravel.log')")

    def test_channels_excludes_channels_without_path(self):
        log_file = LogFile(logging_config=FIXTURE_CONFIG)
        channels = log_file.channels()

        self.assertNotIn('sentry_logs', channels)
        self.assertNotIn('stack', channels)

    def test_find_log_files_skips_variable_paths(self):
        log_file = LogFile(logging_config=FIXTURE_CONFIG)
        files = log_file.find_log_files("storage_path('logs/' . $path . '/laravel.log')")
        self.assertEqual(files, [])

    def test_find_log_files_skips_non_storage_path(self):
        log_file = LogFile(logging_config=FIXTURE_CONFIG)
        files = log_file.find_log_files("'/var/log/laravel.log'")
        self.assertEqual(files, [])

    @patch('LaravelGoto.lib.workspace.get_recursion_files')
    @patch('LaravelGoto.lib.workspace.get_folders')
    def test_find_log_files_returns_matching_files(self, mock_get_folders, mock_get_recursion_files):
        test_dir = self.get_test_dir()
        mock_get_folders.return_value = [test_dir]
        mock_get_recursion_files.return_value = [os.path.join(test_dir, 'storage', 'logs', 'laravel.log')]

        log_file = LogFile(logging_config=FIXTURE_CONFIG)
        files = log_file.find_log_files("storage_path('logs/laravel.log')")
        self.assertIn(os.path.join(test_dir, 'storage', 'logs', 'laravel.log'), files)