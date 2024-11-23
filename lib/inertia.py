from re import compile
from .place import Place


class Inertia:

    inertia_patterns = [
        compile(r"""Route::inertia\s*\([^,]+,\s*['"]([^'"]+)"""),
        compile(r"""Route::inertia\s*\([^,]+,\s*component:\s*['"]([^'"]+)"""),
        compile(r"""Inertia::render\s*\(\s*['"]([^'"]+)"""),
        compile(r"""Inertia::render\s*\(\s*component\s*:\s*['"]([^'"]+)"""),
        compile(r"""inertia\s*\(\s*['"]([^'"]+)"""),
        compile(r"""inertia\s*\(\s*component:\s*['"]([^'"]+)"""),
    ]

    def get_place(self, path, line, lines=''):

        for pattern in self.inertia_patterns:
            matched = pattern.search(line) or pattern.search(lines)
            if (matched and matched.group(1) in path):
                return Place(matched.group(1))

        return False
