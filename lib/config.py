from re import compile
from .place import Place


class Config:
    config_patterns = [
        compile(r"""Config::[^'"]*(['"])([^'"]*)\1"""),
        compile(r"""config\([^'"]*(['"])([^'"]*)\1"""),
    ]

    find_pattern = """(['"]{1})%s\\1\\s*=>"""

    def get_place(self, path, line, lines=''):

        for pattern in self.config_patterns:
            matched = pattern.search(line) or pattern.search(lines)
            if matched is None:
                continue

            if not matched.group(2).startswith(path):
                continue

            split = path.split('.')
            path = 'config/' + split[0] + '.php'
            location = None
            if (2 <= len(split)):
                location = self.find_pattern % (split[1])
            return Place(path, location)

        return False
