import sublime
import sublime_plugin
import re


plugin_settings = None
user_settings = None
extensions = None
patterns = [
    re.compile(r"namespace\s*\(\s*(['\"])\s*([^'\"]+)\1"),
    re.compile(r"['\"]namespace['\"]\s*=>\s*(['\"])([^'\"]+)\1"),
]


class LaravelGotoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        globals()['plugin_settings'] = sublime\
            .load_settings("Plugin.sublime-settings")
        globals()['user_settings'] = sublime.\
            load_settings("Preferences.sublime-settings")
        extensions = user_settings.get("static_extensions", []) +\
            plugin_settings.get("static_extensions")
        globals()['extensions'] = list(map(
            lambda ext: '.' + ext.lower(), extensions))

    def run(self, edit):
        self.window = sublime.active_window()
        path = self.get_path(self.view.sel()[0])
        # print(path)
        if path:
            self.search(path)
        return

    def substr(self, mixed):
        return self.view.substr(mixed)

    def get_selection(self, selected):
        start = selected.begin()
        end = selected.end()

        if start == end:
            line = self.view.line(start)
            delimiters = "\"'"
            while start > line.a:
                if self.substr(start - 1) in delimiters:
                    break
                start -= 1

            while end < line.b:
                if self.substr(end) in delimiters:
                    break
                end += 1

        return sublime.Region(start, end)

    def get_path(self, selected):
        selection = self.get_selection(selected)
        path = self.substr(selection).strip()
        if (self.is_controller(path)):
            namespace = self.get_namespace(selection)
            if namespace:
                path = namespace + '\\' + path
        return path

    def is_controller(self, path):
        return "@" in path or "Controller" in path

    def get_namespace(self, selected):
        functions = self.view.find_by_selector('meta.function-call')
        for function in functions:
            if (not function.contains(selected)):
                continue
            region = self.view.line(function)
            block = self.substr(region).strip()
            for pattern in patterns:
                matched = pattern.search(block)
                if (matched):
                    # print(matched.group(2))
                    return matched.group(2)
        return

    def search(self, path):
        args = {
            "overlay": "goto",
            "show_files": True,
            "text": path
        }

        # open static file
        if (self.is_static_file(path)):
            self.window.run_command("show_overlay", args)
            return

        is_controller = self.is_controller(path)
        if is_controller:
            args["text"] = ''
        else:  # it's a view file
            args["text"] = args["text"].replace('.', '/') + '.blade.php'

        self.window.run_command("show_overlay", args)

        # if it 's Controller path, use insert command to trigger symbol search
        if is_controller:
            self.window.run_command("insert", {
                "characters": path.replace('@', '.php@')
            })
        return

    def is_static_file(self, path):
        # get last 3 chars as extension
        return (path[-3:].lower() in extensions)
