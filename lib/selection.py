import sublime


class Selection(sublime.Region):
    delimiters = "\"'-<>{}"

    def __init__(self, view):
        self.view = view
        self.line = view.line(view.sel()[0].begin())
        scopes = view.scope_name(view.sel()[0].begin())
        self.is_class = 'support.class.php' in scopes
        selected = self.get_selection()
        super(Selection, self).__init__(selected.begin(), selected.end(), -1)

    def substr(self):
        return self.view.substr(self)

    def substr_line(self):
        return self.view.substr(self.line)

    def get_selection(self):
        selected = self.view.sel()[0]
        start = selected.begin()
        end = selected.end()

        if start != end:
            return selected

        selected = self.view.extract_scope(start)
        if self.line.contains(selected):
            if self.is_class:
                selected = self.get_selected_by_delimiters(selected, ',[<', '>])')
            return selected
        return self.get_selected_by_delimiters(selected, self.delimiters)

    def get_selected_by_delimiters(self, selected, start_delims, end_delims=None):
        start = selected.begin()
        end = selected.end()

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

    def get_lines_after_delimiter(self, delimiter = '('):
        lines = [];
        line_number, _ = self.view.rowcol(self.line.a)
        while line_number >= 0:
            point = self.view.text_point(line_number, 0)
            line = self.view.full_line(point)
            text = self.view.substr(line).strip()
            lines.insert(0, text)
            if text.__contains__(delimiter):
                return ''.join(lines);

            line_number = line_number - 1

        return ''

    def get_path(self):
        return self.substr().strip(self.delimiters + ' ')
