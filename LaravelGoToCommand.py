import sublime
import sublime_plugin
import re
import os
from pprint import pprint


class LaravelGoToCommand(sublime_plugin.TextCommand):
    def line_content(self, event):
      vector = (event["x"], event["y"])
      point = self.view.window_to_text(vector)
      region = self.view.word(point)
      line_range = self.view.line(region)
      text = self.view.substr(line_range).strip()
      return text;

    def get_path(self, line_content):
      # pattern = re.compile("(['\"])([^'\"]+)\\1")
      pattern = re.compile("(view|@include)\\s*\\(\\s*(['\"])([^'\"]+)\\2")
      matched = pattern.match(line_content)
      pprint(matched)
      if matched:
        return matched.group(2).replace('.', '/')
      return False

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
      line_content = self.line_content(event)
      path = self.get_path(line_content)
      pprint(path)
      if path:
        self.window.run_command("show_overlay", {
          "overlay": "goto",
          "show_files": True,
          "text": path
        })
      return

    def want_event(self):
      return True