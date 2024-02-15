import os
import subprocess
import json

from .place import Place
from . import workspace
from .setting import Setting
from .logging import info, exception

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
        info('artisan', self.artisan)
        info('routes folder', self.dir)
        if not self.artisan or not self.dir:
            return

        is_routes_changed = self.is_changed(filepath)
        info('routes changed', is_routes_changed)
        if not is_routes_changed:
            return
        workspace.set_unchanged(self.dir)

        php = Setting().get('php_bin')
        if not php:
            return

        args = [
            php,
            self.artisan,
            'route:list',
            '--json'
        ]

        try:
            output = subprocess.check_output(
                args,
                cwd='/',
                stderr=subprocess.STDOUT,
                shell=os.name == 'nt'
                )

        except subprocess.CalledProcessError as e:
            exception('route:list failed', e)
            return
        except FileNotFoundError as e:
            exception('file not found', e)
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

    def is_changed(self, filepath=None):
        return workspace.is_changed(self.dir, filepath)

    def all(self):
        self.update()
        return routes
