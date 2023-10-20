from .place import Place
from . import workspace
import subprocess
import json
from .setting import Setting


class Router:
    def __init__(self):
        for folder in workspace.get_folders():
            self.artisan = workspace.get_path(
                folder,
                'artisan',
                True
                )
            if self.artisan:
                return

    def all(self):
        routes = {}
        if not self.artisan:
            return routes

        php = Setting().get('php_bin')
        if not php:
            return routes

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
            return routes

        output = output.decode('utf-8')
        try:
            route_rows = json.loads(output)
        except ValueError:
            return routes

        for route_row in route_rows:
            if 'Closure' == route_row['action']:
                continue

            path, action = route_row['action'].split('@')
            if action:
                routes[route_row['name']] = Place(
                    workspace.class_2_file(path),
                    location=action
                    )

        return routes
