import sublime
from re import sub


class Selection(sublime.Region):
    delimiters = """<("'[,)> """

    def __init__(self, view, point=None):
        self.view = view
        self.region = view.sel()[0]
        if point:
            self.region = sublime.Region(point, point)
        self.line = view.line(self.region)

        scopes = view.scope_name(self.region.begin())
        self.is_class = 'support.class.php' in scopes

        selected = self.get_selection()
        super(Selection, self).__init__(selected.begin(), selected.end(), -1)

    def substr(self):
        return self.view.substr(self)

    def substr_line(self):
        return self.view.substr(self.line)

    def get_selection(self):
        if self.region.begin() != self.region.end():
            return self.region

        return self.get_selected_by_delimiters(self.delimiters)

    def get_selected_by_delimiters(self, start_delims, end_delims=None):
        start = self.region.begin()
        end = self.region.end()

        if (end_delims is None):
            end_delims = start_delims
        while start > self.line.a:
            if self.view.substr(start - 1) in start_delims:
                break
            start -= 1

        while end < self.line.b:
            if self.view.substr(end) in end_delims:
                break
            end += 1
        return sublime.Region(start, end)

    def get_line(self):
        return self.substr_line().strip()

    def get_lines_after_delimiter(self, delimiter='('):
        lines = []
        line_number, _ = self.view.rowcol(self.line.a)
        while line_number >= 0:
            point = self.view.text_point(line_number, 0)
            line = self.view.full_line(point)
            text = self.view.substr(line).strip()
            lines.insert(0, text)
            if text.__contains__(delimiter) and not text.startswith('->'):
                return ''.join(lines)

            line_number = line_number - 1

        return ''

    def get_path(self):
        path = self.substr().strip(self.delimiters + ' ')
        # remove the rest of string after {
        path = sub('{.*', '', path)
        # remove the rest of string after $
        path = sub('\\$.*', '', path)
        # remove dot at the end
        path = path.rstrip('.')

        return path
