import sublime
import sublime_plugin
import re
import os

class LaravelGotoCommand(sublime_plugin.TextCommand):
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
      args = {
        "overlay": "goto",
        "show_files": True,
        "text": path
      }

      # open static file
      if (self.is_static_file(path)):
        self.window.run_command("show_overlay", args)
        return

      is_controller = "@" in path or "Controller" in path
      if is_controller:
        args["text"] = ''
      else: # it's a view file
        args["text"] = args["text"].replace('.', '/') + '.blade.php';

      self.window.run_command("show_overlay", args)

      # if it's Controller path, use insert command to trigger symbol search
      if is_controller:
        self.window.run_command("insert", {
            "characters": path.replace('@', '.php@')
        })
      return

    def is_static_file(self, path) -> bool:
      for ext in self.extensions:
        if path.endswith('.' + ext):
          return True
      return False

    def run(self, edit):
      self.window = sublime.active_window()
      if (len(self.window.folders()) == 0):
        return

      default = sublime.load_settings("Plugin.sublime-settings")
      settings = sublime.load_settings("Preferences.sublime-settings")
      self.extensions = settings.get('static_extensions', default.get('static_extensions'))

      path = self.get_text(self.view.sel()[0])
      print(path)
      if path:
        self.search(path)
      return
