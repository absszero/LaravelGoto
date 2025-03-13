import os
import subprocess
import json

from .place import Place
from . import workspace
from .setting import Setting
from .logging import info, exception
from .route_item import RouteItem


class Router:
    artisan = None
    dir = None

    named_routes = {}
    uri_routes = []

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

        self.named_routes.clear()
        self.uri_routes.clear()

        for route in route_rows:
            if 'Closure' == route['action']:
                continue

            path = route['action']
            action = '__invoke'
            if '@' in route['action']:
                path, action = route['action'].split('@')

            place = Place(
                workspace.class_2_file(path) + '@' + action,
            )
            place.is_controller = True

            self.named_routes[route['name']] = place
            self.uri_routes.append(RouteItem(route, place))

        return True

    def is_changed(self, filepath=None):
        return workspace.is_changed(self.dir, filepath)

    def all(self):
        self.update()
        return self.named_routes

    def uris(self):
        self.update()
        return self.uri_routes
