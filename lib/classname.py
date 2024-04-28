from re import compile
from .place import Place


class ClassName:
    pattern = compile(r"""([A-Z][\w]+[\\])+[A-Z][\w]+""")

    def get_place(self, path, line, lines=''):
        matched = self.pattern.search(line)
        if not matched:
            return False

        return Place(path + '.php')
