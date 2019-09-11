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
config_patterns = [
    re.compile(r"Config::[^'\"]*(['\"])([^'\"]*)\1"),
    re.compile(r"config\([^'\"]*(['\"])([^'\"]*)\1"),
]

env_pattern = re.compile(r"env\([^'\"]*(['\"])([^'\"]*)\1")


class Place:
    def __init__(self, path, is_controller):
        self.path = path
        self.is_controller = is_controller


class LaravelGotoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        globals()['plugin_settings'] = sublime\
            .load_settings("Plugin.sublime-settings")
        globals()['user_settings'] = sublime.\
            load_settings("Preferences.sublime-settings")
        extensions = user_settings.get("static_extensions", []) +\
            plugin_settings.get("static_extensions", [])
        globals()['extensions'] = list(map(
            lambda ext: ext.lower(), extensions))

    def run(self, edit):
        self.window = sublime.active_window()
        selection = self.get_selection(self.view.sel()[0])
        place = self.get_place(selection)
        self.search(place)
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

    def get_place(self, selected):
        region = self.view.line(selected.a)
        line = self.substr(region).strip()
        path = self.substr(selected).strip()
        is_controller = self.is_controller(path)
        if (is_controller):
            path = path.replace('@', '.php@')
            # it's not absolute path namespace
            if '\\' != path[0]:
                namespace = self.get_namespace(selected)
                if namespace:
                    path = namespace + '\\' + path

        elif(self.is_static_file(path)):
            pass

        elif(self.is_config(path, line)):
            path = 'config/' + path.split('.')[0] + '.php'

        elif(self.is_env(path, line)):
            path = '.env'

        else:
            # remove Blade Namespace
            path = path.split(':')[-1]
            path = path.replace('.', '/') + '.blade.php'
        return Place(path, is_controller)

    def is_controller(self, path):
        return "@" in path or "Controller" in path

    def is_config(self, path, line):
        for pattern in config_patterns:
            matched = pattern.search(line)
            if (matched and path == matched.group(2)):
                return True
        return False

    def is_static_file(self, path):
        return (path.split('.')[-1].lower() in extensions)

    def is_env(self, path, line):
        matched = env_pattern.search(line)
        return (matched and path == matched.group(2))

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
                    return matched.group(2)
        return

    def search(self, place):
        args = {
            "overlay": "goto",
            "show_files": True,
            "text": place.path
        }

        if (not place.is_controller):
            self.window.run_command("show_overlay", args)
        else:
            args["text"] = ''
            self.window.run_command("show_overlay", args)
            self.window.run_command("insert", {
                "characters": place.path
            })
        return
