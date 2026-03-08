from re import compile
from .place import Place


class Helper:
    def get_place(self, path, line, lines=''):
        pattern = compile(r"""([\w^_]+)_path\(\s*(['"])([^'"]*)\2""")
        matched = pattern.search(line) or pattern.search(lines)
        if (matched and path == matched.group(3)):
            prefix = matched.group(1) + '/'
            if 'base/' == prefix:
                prefix = ''
            elif 'resource/' == prefix:
                prefix = 'resources/'

            return Place(prefix + path)

        # to_action
        pattern = compile(r"""to_action\(\s*\[([^,]+),\s*(['"])([^'"]*)\2""")
        matched = pattern.search(line) or pattern.search(lines)
        if (matched and path == matched.group(3)):
            return Place(matched.group(1).replace('::class', '').replace('\\', '/') + '.php@' + matched.group(3))

        return False
