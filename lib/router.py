from .place import Place
from . import workspace
import subprocess
import json
from .setting import Setting
from .logging import debug, exception

routes = {}


class Router:
    artisan = None
    dir = None

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
        debug('artisan', self.artisan)
        debug('routes folder', self.dir)
        if not self.artisan or not self.dir:
            return

        is_routes_changed = workspace.is_changed(self.dir, filepath)
        debug('routes changed', is_routes_changed)
        if not is_routes_changed:
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
        debug('args', args)

        try:
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            exception('check_output', e)
            return
        except FileNotFoundError as e:
            exception('check_output', e)
            return

        output = output.decode('utf-8')
        try:
            route_rows = json.loads(output)
        except ValueError as e:
            exception('json.loads', e)
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
