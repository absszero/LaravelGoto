import sublime
import sublime_plugin
import re
import os

class LaravelGoToCommand(sublime_plugin.TextCommand):
    def substr(self, mixed) -> str:
      return self.view.substr(mixed)

    def get_text(self, selected) -> str:
      start = selected.begin()
      end = selected.end()

      if start != end:
          return self.substr(selected).strip()

      delimiters = "\"'"
      line = self.view.line(start)
      while start > line.a:
          if self.substr(start - 1) in delimiters:
              break
          start -= 1

      while end < line.b:
          if self.substr(end) in delimiters:
              break
          end += 1
      return self.substr(sublime.Region(start, end)).strip()

    def search(self, path) -> str:
      text = path.replace('.', '/');
      is_symbol = "@" in path or "Controller" in path
      args = {
        "overlay": "goto",
        "show_files": True,
        "text": text + '.blade.php'
      }
      if is_symbol:
        args["text"] = ''

      self.window.run_command("show_overlay", args)

      if is_symbol:
        self.window.run_command("insert", {
            "characters": text.replace('@', '.php@')
        })
      return

    def run(self, edit):
      self.window = sublime.active_window()
      if (len(self.window.folders()) == 0):
        return

      path = self.get_text(self.view.sel()[0])
      print(path)
      if path:
        self.search(path)
      return
