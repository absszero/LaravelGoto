import sublime
import re
from .place import Place
from . import workspace
import os

class Console:
    def __init__(self, console_kernel=None):
        self.console_kernel = console_kernel
        if self.console_kernel:
            return
        for folder in workspace.get_folders():
            fullpath = workspace.get_path(folder, 'app/Console/Kernel.php', True)
            if not fullpath:
                continue

            self.folder = os.path.dirname(fullpath)
            self.console_kernel = workspace.get_file_content(fullpath)
            if self.console_kernel:
                return

    def all(self):
        commands = {}
        if not self.console_kernel:
            return commands

        files = self.collect_files()
        commands = self.collect_file_cmds(files)
        commands.update(self.collect_registered_cmds())
        return commands


    def get_command_signature(self, content):
        match = re.search("""\$signature\s*=\s*['"]([^\s'"]+)""", content)
        if match:
            return match.group(1)
        return ''


    def collect_files(self):
        files = []
        match = re.search("""function commands\([^\)]*[^{]+([^}]+)""", self.console_kernel)
        if not match:
            return files

        for match in re.findall("""\$this->load\(\s*__DIR__\.['"]([^'"]+)""", match.group(1)):
            if match.startswith('/'):
                match = match[1:]

            folder = os.path.join(self.folder, match)
            files += workspace.get_recursion_files(folder)
        return files


    def collect_file_cmds(self, files):
        commands = {};
        for file in files:
            content = workspace.get_file_content(file)
            signature = self.get_command_signature(content)
            if signature:
                commands[signature] = Place(os.path.basename(file), uri=file)

        return commands;


    def collect_registered_cmds(self):
        commands = {};
        match = re.search("""\$commands\s*=\s*\[([^\]]+)""", self.console_kernel, re.M);
        if not match:
            return commands


        classes = match.group(1).splitlines();
        for class_name in classes:
            filename = class_name.replace(',', '').replace('::class', '').replace('\\', '/').strip() + '.php';
            if filename.startswith('/'):
                filename = filename[1:]

            if filename.startswith('App/'):
                filename = filename.replace('App/', 'app/', 1)

            if filename == '.php':
                continue

            for folder in workspace.get_folders():
                uri = workspace.get_path(folder, filename, True)
                if not uri:
                    continue;
                content = workspace.get_file_content(uri)
                signature = self.get_command_signature(content)
                if signature:
                    commands[signature] = Place(filename, uri=uri)

        return commands

