from re import compile
from .place import Place


class Blade:
    def get_place(self, path, line, lines=''):

        blade_patterns = [
            compile(r"""view\(\s*(['"])([^'"]*)\1"""),
            compile(r"""\$view\s*=\s*(['"])([^'"]*)\1"""),
            compile(r"""view:\s*(['"])([^'"]*)\1"""),
            compile(r"""view\(\s*['"][^'"]*['"],\s*(['"])([^'"]*)\1"""),
            compile(r"""[lL]ayout\(\s*(['"])([^'"]*)\1"""),
            compile(r"""['"]layout['"]\s*=>\s*(['"])([^'"]*)\1"""),
            compile(r"""@include(If\b)?\(\s*(['"])([^'"]*)\2"""),
            compile(r"""@extends\(\s*(['"])([^'"]*)\1"""),
            compile(r"""@include(When|Unless\b)?\([^'"]+(['"])([^'"]+)"""),
            compile(r"""View::exists\(\s*(['"])([^'"]*)\1"""),
            compile(r"""View::composer\(\s*(['"])([^'"]*)\1"""),
            compile(r"""View::creator\(\s*(['"])([^'"]*)\1"""),
            compile(r"""(resources\/views[^\s'"-]+)"""),
        ]
        for pattern in blade_patterns:
            matched = pattern.search(line) or pattern.search(lines)
            if matched is None:
                continue

            groups = matched.groups()
            if path == groups[-1]:
                path = groups[-1].strip()
                path = self.transform_blade(path)
                return Place(path)

        multi_views_patterns = [
            compile(
                r"""@includeFirst\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""
            ),
            compile(
                r"""View::composer\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""
            ),
            compile(r"""@each\(['"][^'"]+['"]\s*,[^,]+,[^,]+,[^)]+"""),
            compile(r"""View::first[^'"]*(['"])([^'"]*)\1"""),
        ]
        for pattern in multi_views_patterns:
            if pattern.search(line) or pattern.search(lines):
                path = self.transform_blade(path)
                return Place(path)

        return False

    def transform_blade(self, path):
        split = path.split(':')
        vendor = ''
        # vendor or namespace
        if (3 == len(split)):
            # vendor probably is lowercase
            if (split[0] == split[0].lower()):
                vendor = split[0] + '/'

        path = split[-1]
        path = vendor + path.replace('.', '/')
        if path.endswith('/blade/php'):
            path = path[:-1*len('/blade/php')]

        path += '.blade.php'
        return path
