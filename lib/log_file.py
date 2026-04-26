import re
import os
from . import workspace
from pathlib import Path


class LogFile:
    def __init__(self, logging_config=None):
        self.logging_config = logging_config
        self.folder = None

        if self.logging_config is not None:
            return

        for folder in workspace.get_folders():
            fullpath = workspace.get_path(folder, 'config/logging.php')
            if not fullpath:
                continue

            self.folder = folder
            self.logging_config = workspace.get_file_content(fullpath)
            if self.logging_config:
                return

    def channels(self):
        '''
        Parse config/logging.php and return a dict of {channel_name: path_expression}
        for channels that have a 'path' key.
        '''
        result = {}
        if not self.logging_config:
            return result

        channel_pattern = re.compile(r"""['"]([\w]+)['"]\s*=>\s*\[([^\]]+)""")
        for match in channel_pattern.finditer(self.logging_config):
            channel_name = match.group(1)
            channel_config = match.group(2)

            path_match = re.search(r"""['"]path['"]\s*=>\s*([^,\n]+)""", channel_config)
            if not path_match:
                continue

            path_value = path_match.group(1).strip().rstrip(',').strip()
            result[channel_name] = path_value

        return result

    def find_log_files(self, path_expression):
        '''
        Given a path expression like storage_path('logs/laravel.log'),
        find matching .log files on disk.
        Returns a sorted list of absolute file paths (newest filename first).
        '''
        # Skip paths with PHP variables — can't resolve them statically
        if '$' in path_expression:
            return []

        storage_match = re.search(
            r"""storage_path\s*\(\s*['"](logs/[^'"]+)""",
            path_expression
        )
        if not storage_match:
            return []

        log_path = Path(storage_match.group(1))
        log_folder = log_path.parent
        log_file_pattern = log_path.name[:-4] + '*.log'
        for folder in workspace.get_folders():
            storage_dir = os.path.join(folder, 'storage', log_folder)
            files = workspace.get_recursion_files(storage_dir, log_file_pattern)
            files.sort(reverse=True)
            return files

        return []
