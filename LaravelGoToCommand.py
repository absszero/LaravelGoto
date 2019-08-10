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

    def run(self, edit, event):
      self.window = sublime.active_window()
      if (len(self.window.folders()) == 0):
        return

      fn = self.get_namespace(self.window.active_view())

      path = self.get_text(self.view.sel()[0])
      # pprint(path)
      # if path:
      #   self.search(path)
      return

    def want_event(self):
      return True
