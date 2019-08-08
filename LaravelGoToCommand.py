import sublime
import sublime_plugin
import re
import os
from pprint import pprint


class LaravelGoToCommand(sublime_plugin.TextCommand):
    def get_text(self, region) -> str:
      """Returns selection. If selection contains no characters, expands it
      until hitting delimiter chars.
      """
      start = region.begin()  # type: int
      end = region.end()  # type: int

      if start != end:
          sel = self.view.substr(sublime.Region(start, end))  # type: str
          return sel.strip()

      # nothing is selected, so expand selection to nearest delimiters
      view_size = self.view.size()  # type: int
      delimiters = "\"'"

      # move the selection back to the start of the url
      while start > 0:
          if self.view.substr(start - 1) in delimiters:
              break
          start -= 1

      # move end of selection forward to the end of the url
      while end < view_size:
          if self.view.substr(end) in delimiters:
              break
          end += 1
      sel = self.view.substr(sublime.Region(start, end))
      return sel.strip()

    def on_done(self, text):
        try:
            line = int(text)
            if self.window.active_view():
                self.window.active_view().run_command("goto_line", {"line": line})
        except ValueError:
            pass


    def run(self, edit, event):
      if (len(sublime.active_window().folders()) == 0):
        return
      self.window = sublime.active_window()
      path = self.get_text(self.view.sel()[0])
      if path:
        self.window.run_command("show_overlay", {
          "overlay": "goto",
          "show_files": True,
          "text": path.replace('.', '/')
        })
      return

    def want_event(self):
      return True

# a = LaravelGoToCommand(sublime_plugin.TextCommand)
# a.get_path('"admins/guests/index");')
