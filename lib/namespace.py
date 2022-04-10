import sublime
from re import compile

patterns = [
    (compile(r"""(controller)\s*\(\s*['"]?([^'")]+)"""), False),
    (compile(r"""resource\s*\(\s*['"][^'"]+['"]\s*,\s*(['"]?)([^,'"]+)"""), False),
    (compile(r"""namespace\s*\(\s*(['"])\s*([^'"]+)\1"""), True),
    (compile(r"""['"]namespace['"]\s*=>\s*(['"])([^'"]+)\1"""), True),
]


class Namespace:
    def __init__(self, view):
        self.fullText = view.substr(sublime.Region(0, view.size()))
        self.length = len(self.fullText)

    def find(self, blocks):
        ''' find the namespace of the selection'''
        for block in blocks:
            if block['is_namespace']:
                return block['namespace']
        return False

    def get_blocks(self, selection):
        '''get all closure blocks'''
        blocks = []
        for pattern, isNamespace in patterns:
            for match in pattern.finditer(self.fullText):
                start = match.start()
                if selection.a < start:
                    continue

                end = self.get_end_position(start)
                if selection.b > end:
                    continue

                blocks.append({
                    'is_namespace': isNamespace,
                    'namespace': match.group(2).strip().replace('::class', ''),
                    'range': sublime.Region(start, end)
                })
        return blocks

    def get_end_position(self, start):
        '''get the end position from the start position'''
        result = []
        while self.length > start:
            if '{' == self.fullText[start]:
                result.append(start)
            elif '}' == self.fullText[start]:
                if 0 != len(result):
                    result.pop()
                if 0 == len(result):
                    return start
            start = start + 1

        return start
