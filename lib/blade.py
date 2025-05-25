from re import compile
from .place import Place


class Blade:
    blade_patterns = [
        compile(r"""\b(?:view|markdown)\b\(\s*(['"])([^'"]*)\1"""),
        compile(r"""\$view\s*=\s*(['"])([^'"]*)\1"""),
        compile(r"""\b(?:view|text|html|markdown)\b\s*:\s*(['"])([^'"]*)\1"""),
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

    multi_views_patterns = [
        compile(
            r"""@includeFirst\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""
        ),
        compile(
            r"""View::composer\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""
        ),
        compile(r"""view\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""),
        compile(r"""@each\(['"][^'"]+['"]\s*,[^,]+,[^,]+,[^)]+"""),
        compile(r"""View::first[^'"]*(['"])([^'"]*)\1"""),
    ]

    fragment_patterns = [
        compile(r"""->fragment\(\s*['"]([^'"]+)"""),
        compile(r"""->fragmentIf\(\s*.*,\s*['"]([^'"]+)""")
    ]

    multi_fragments_patterns = [
        compile(r"""->fragments\(\s*\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\s*\]"""),
        compile(r"""->fragmentsIf\(\s*.*,\s*\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\s*\]""")
    ]

    location_pattern = """fragment\\(\\s*['"]%s['"]\\s*\\)"""

    def get_place(self, path, line, lines=''):

        for pattern in self.blade_patterns:
            matched = pattern.search(line) or pattern.search(lines)
            if matched is None:
                continue

            groups = matched.groups()
            if path == groups[-1]:
                path = groups[-1].strip()
                path = self.transform_blade(path)
                return Place(path)

        for pattern in self.multi_views_patterns:
            if pattern.search(line) or pattern.search(lines):
                path = self.transform_blade(path)
                return Place(path)

        for frg_pattern in self.fragment_patterns:
            frg_matched = frg_pattern.search(lines) or frg_pattern.search(line)
            if frg_matched is None:
                continue

            for pattern in self.blade_patterns:
                matched = pattern.search(line) or pattern.search(lines)
                if matched is None:
                    continue

                file = matched.groups()[-1].strip()
                file = self.transform_blade(file)
                location = self.location_pattern % path
                return Place(file, location)

        for frg_pattern in self.multi_fragments_patterns:
            frg_matched = frg_pattern.search(lines) or frg_pattern.search(line)
            if frg_matched is None:
                continue

            for pattern in self.blade_patterns:
                matched = pattern.search(line) or pattern.search(lines)
                if matched is None:
                    continue

                file = matched.groups()[-1].strip()
                file = self.transform_blade(file)
                location = self.location_pattern % path
                return Place(file, location)

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
