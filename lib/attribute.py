from re import compile
from .place import Place


class Attribute:
    patterns = [
        compile(r"""#\[([^(]+)\('([^"']+)"""),
    ]

    location_pattern = """['"]%s['"]\\s*=>"""

    files = {
        'Auth': 'config/auth.php',
        'Cache': 'config/cache.php',
        'DB': 'config/database.php',
        'Log': 'config/logging.php',
        'Storage': 'config/filesystems.php',
    }

    def get_place(self, path, line, lines=''):
        for pattern in self.patterns:
            matched = pattern.search(line) or pattern.search(lines)
            if matched == None:
                continue

            groups = matched.groups()
            if path != groups[1]:
                continue

            # Config file
            if 'Config' == groups[0]:
                split = path.split('.')
                path = 'config/' + split[0] + '.php'
                location = None
                if (2 <= len(split)):
                    location = self.location_pattern % (split[1])
                return Place(path, location)

            if groups[0] in self.files:
                path = self.files.get(groups[0])
                location = self.location_pattern % (groups[1])
                return Place(path, location)

        return False
