import sublime
from re import compile

patterns = [
    compile(r"namespace\s*\(\s*(['\"])\s*([^'\"]+)\1"),
    compile(r"['\"]namespace['\"]\s*=>\s*(['\"])([^'\"]+)\1"),
]

fullText = ''
length = 0


def find(view, selection):
    ''' find the namespace of the selection'''
    fullText = view.substr(sublime.Region(0, view.size()))
    length = len(fullText)

    blocks = get_blocks(selection)
    for closure in blocks:
        if closure['range'].contains(selection):
            return closure['namespace']
    return ''


def get_blocks(selection):
    '''get all closure blocks'''
    blocks = []
    for pattern in patterns:
        for match in pattern.finditer(fullText):
            start = match.start()
            if selection.a > start:
                end = getEndPosition(start)
                blocks.append({
                    'namespace': match.group(2),
                    'range': sublime.Region(start, end)
                })
    return blocks


def getEndPosition(start):
    '''get the end position from the start position'''
    result = []
    while length > start:
        if ('{' == fullText[start]):
            result.append(start)
        elif ('}' == fullText[start]):
            result.pop()
            if (0 == len(result)):
                return start
        start = start + 1

    return start
