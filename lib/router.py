from .place import Place
from . import workspace
import subprocess
import json
from .setting import Setting

routes = {}


class Router:
    def __init__(self):
        for folder in workspace.get_folders():
            self.artisan = workspace.get_path(folder, 'artisan')
            self.dir = workspace.get_folder_path(folder, 'routes')
            if self.dir:
                return

    def update(self, filepath=None):
        '''
        update routes if routes folder's files were changed
        '''
        if not self.artisan or not self.dir:
            return

        if not workspace.is_changed(self.dir, filepath):
            return
        workspace.set_unchange(self.dir)

        php = Setting().get('php_bin')
        if not php:
            return

        args = [
            php,
            self.artisan,
            'route:list',
            '--json',
            '--columns=name,action'
        ]

        try:
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError:
            return

        output = output.decode('utf-8')
        try:
            route_rows = json.loads(output)
        except ValueError:
            return

        for route_row in route_rows:
            if 'Closure' == route_row['action']:
                continue

            path, action = route_row['action'].split('@')
            if action:
                routes[route_row['name']] = Place(
                    workspace.class_2_file(path),
                    location=action
                    )

    def all(self):
        self.update()
        return routes
