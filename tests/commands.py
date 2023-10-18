from sublime_plugin import TextCommand
from sublime import Region


class SetupFixtureCommand(TextCommand):
    def run(self, edit, text):
        self.view.replace(edit, Region(0, self.view.size()), text)

        if '|' not in text:
            return
        cursor_placeholders = self.view.find_all('\\|')
        if not cursor_placeholders:
            return

        self.view.sel().clear()
        for i, cursor_placeholder in enumerate(cursor_placeholders):
            self.view.sel().add(cursor_placeholder.begin() - i)
            self.view.replace(
                edit,
                Region(
                    cursor_placeholder.begin() - i,
                    cursor_placeholder.end() - i),
                ''
                )
