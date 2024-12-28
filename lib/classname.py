from re import compile
from .place import Place


class ClassName:
    patterns = [
        compile(r"""([A-Z][\w]+[/\\])+[A-Z][\w]+""")
    ]

    def get_place(self, path, line, lines=''):
        for pattern in self.patterns:

            matched = pattern.search(line) or pattern.search(lines)
            if matched:
                return Place(path + '.php')

        return False
