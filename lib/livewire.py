from re import compile
from .place import Place


class Livewire:

    patterns = [
        compile(r"""livewire:([^\s"'>]+)"""),
        compile(r"""@livewire\s*\(\s*['"]([^'"]+)"""),

    ]

    def get_place(self, path, line, lines=''):

        for pattern in self.patterns:
            matched = pattern.search(line) or pattern.search(lines)
            if matched:
                path = self.camel_case(matched.group(1))
                path = path.replace('.', '/') + '.php'
                return Place(path)

        return False

    def camel_case(self, snake_str):
        components = snake_str.split('-')
        return components[0].title() + ''.join(x.title() for x in components[1:])
