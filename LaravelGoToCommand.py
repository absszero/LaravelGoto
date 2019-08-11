import sublime
import sublime_plugin
import re
import os
from pprint import pprint

class LaravelGoToCommand(sublime_plugin.TextCommand):
    def get_text(self, selected) -> str:
      start = selected.begin()
      end = selected.end()

      if start != end:
          return self.view.substr(selected).strip()

      # nothing is selected, so expand selection to nearest delimiters
      delimiters = "\"'"

      # move the selection back to the start of the url
      while start > 0:
          if self.view.substr(start - 1) in delimiters:
              break
          start -= 1

      # move end of selection forward to the end of the url
      view_size = self.view.size()  # type: int
      while end < view_size:
          if self.view.substr(end) in delimiters:
              break
          end += 1
      return self.view.substr(sublime.Region(start, end)).strip()

    def search(self, path):
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

    def get_namespace(self, view):
        sel = view.sel()[0]
        function_regions = view.find_by_selector('meta.function.closure')
        function_regions = view.find_by_selector('meta.function')

        # function_regions = view.find_by_selector('meta.array.php')
        # 'namespace' =>'YOUR_NAMESPACE'
        # pattern = re.compile(r"['\"]namespace['\"]\s*=>\s*(['\"])([^'\"]+)\1")
        namespace = ''
        methods = []
        for idx, r in enumerate(view.find_by_selector('variable.function')):
            word = self.view.word(r)
            method = self.view.substr(word).strip()
            if method == 'group' or method == 'namespace':
              methods.append(r);
        for r in methods:
            word = self.view.word(r)
            method = self.view.substr(word).strip()


        function_regions = view.find_by_selector('meta.function meta.block punctuation.section.block.end')
        for r in function_regions:
            word = self.view.word(r)
            method = self.view.substr(word).strip()
            pprint(method)
            pprint(r)
        print("\n")

        return

    def run(self, edit):
      self.window = sublime.active_window()
      # if (len(self.window.folders()) == 0):
      #   return

      # fn = self.get_namespace(self.window.active_view())

      path = self.get_text(self.view.sel()[0])
      if path:
        self.search(path)
      return
