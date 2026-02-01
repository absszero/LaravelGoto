from re import compile
from .place import Place


class Logging:
    patterns = [
        compile(r"""Log::channel[^'"]*['"]([^'"]*)"""),
    ]

    multi_channel_patterns = [
        compile(r"""Log::stack\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""),
    ]

    find_pattern = """(['"]{1})%s\\1\\s*=>"""

    def get_place(self, path, line, lines=''):

        for pattern in self.patterns:
            matched = pattern.search(line) or pattern.search(lines)
            if matched is None:
                continue

            groups = matched.groups()
            if path == groups[-1]:
                location = self.find_pattern % (groups[-1])
                return Place('config/logging.php', location)

        for pattern in self.multi_channel_patterns:
            if pattern.search(line) or pattern.search(lines):
                location = self.find_pattern % (path)
                return Place('config/logging.php', location)

        return False
