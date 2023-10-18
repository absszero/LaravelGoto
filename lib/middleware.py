import re
from .place import Place
from . import workspace


class Middleware:
    def __init__(self, http_kernel=None):
        self.http_kernel = http_kernel
        if self.http_kernel:
            return
        for folder in workspace.get_folders():
            self.http_kernel = workspace.get_file_content(
                folder,
                'app/Http/Kernel.php'
                )
            if self.http_kernel:
                return

    def all(self):
        middlewares = {}
        if not self.http_kernel:
            return middlewares

        # Before Laravel 10, middlewareAliases was called routeMiddleware.
        # They work the exact same way.
        aliasPattern = r"""(\$\bmiddlewareAliases\b|\$\brouteMiddleware\b)\s*=\s*\[([^;]+)"""  # noqa: E501

        match = re.search(aliasPattern, self.http_kernel, re.M)
        if match is None:
            return middlewares

        classnames = self.collect_classnames(self.http_kernel)

        pattern = re.compile(r"""['"]([^'"]+)['"]\s*=>\s*([^,\]]+)""")
        for match in pattern.findall(match.group()):
            classname = match[1].replace('::class', '').strip()
            if classnames.get(classname):
                classname = classnames.get(classname)
            classname = classname.replace('\\', '/') + '.php'

            if classname.startswith('/'):
                classname = classname[1:]

            middlewares[match[0]] = Place(classname)

        return middlewares

    def collect_classnames(self, content):
        classnames = {}
        pattern = re.compile(r"use\s+([^\s]+)\s+as+\s+([^;]+)")
        for match in pattern.findall(content):
            classnames[match[1]] = match[0].strip()

        return classnames
