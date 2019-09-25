import sublime
import sublime_plugin
import re
import os


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
lang_patterns = [
    re.compile(r"__\([^'\"]*(['\"])([^'\"]*)\1"),
    re.compile(r"@lang\([^'\"]*(['\"])([^'\"]*)\1"),
    re.compile(r"trans\([^'\"]*(['\"])([^'\"]*)\1"),
    re.compile(r"trans_choice\([^'\"]*(['\"])([^'\"]*)\1"),
]

env_pattern = re.compile(r"env\(\s*(['\"])([^'\"]*)\1")

excludes_dir = ['.git', '.svn', 'node_modules', 'vendor']


class Place:
    def __init__(self, path, is_controller, find):
        self.path = path
        self.is_controller = is_controller
        self.find = find


class LaravelGotoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        globals()['plugin_settings'] = sublime\
            .load_settings("Plugin.sublime-settings")
        globals()['user_settings'] = sublime.\
            load_settings("Preferences.sublime-settings")
        # combine extensions
        extensions = user_settings.get("static_extensions", []) +\
            plugin_settings.get("static_extensions", [])
        # make sure extensions are lower case
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
        find = None

        if (is_controller):
            path = path.replace('@', '.php@')
            # it's not absolute path namespace
            if '\\' != path[0]:
                namespace = self.get_namespace(selected)
                if namespace:
                    path = namespace + '\\' + path

        elif(self.is_static_file(path)):
            pass

        elif(self.is_env(path, line)):
            dirs = self.get_dir('.env', 'artisan')
            if (dirs):
                find = path
                path = os.path.join(dirs, '.env')
            else:
                path = '.env'

        elif(self.is_config(path, line)):
            splited = path.split('.')
            path = splited[0] + '.php'
            dirs = self.get_dir('config', 'database')
            if (dirs):
                find = True
                path = os.path.join(dirs, 'config', path)
                if (2 <= len(splited)):
                    find = splited[1]
                    find = "(['\"]{1})" + find + "\\1\\s*=>"
        elif(self.is_lang(path, line)):
            # a package lang file
            if '::' in path:
                path = path.split(':')[-1] + '.php'
            else:
                splited = path.split('.')
                path = 'resources/lang/' + splited[0] + '.php'

        else:
            # remove Blade Namespace
            path = path.split(':')[-1]
            path = path.replace('.', '/') + '.blade.php'
        return Place(path, is_controller, find)

    def is_controller(self, path):
        return "@" in path or "Controller" in path

    def is_config(self, path, line):
        for pattern in config_patterns:
            matched = pattern.search(line)
            if (matched and path == matched.group(2)):
                return True
        return False

    def is_lang(self, path, line):
        for pattern in lang_patterns:
            matched = pattern.search(line)
            if (matched and path == matched.group(2)):
                return True
        return False

    def is_static_file(self, path):
        return (path.split('.')[-1].lower() in extensions)

    def is_env(self, path, line):
        matched = env_pattern.search(line)
        return (matched and path == matched.group(2))

    def get_dir(self, target1, target2, folders=False):
        if (folders is False):
            folders = self.window.folders()
        for folder in folders:
            files = os.listdir(folder)
            if (target1 in files and target2 in files):
                return folder
            '''
            rules:
            1. not in excludes_dir
            2. no dot in filename
            3. is a folder
            '''
            sub_folders = [
                f for f in files if
                f not in excludes_dir and
                '.' not in f and
                os.path.isdir(os.path.join(folder, f))
            ]
            if (len(sub_folders)):
                # get full path
                sub_folders = list(map(
                    lambda f: os.path.join(folder, f), sub_folders
                ))
                find = self.get_dir(target1, target2, sub_folders)
                if (find):
                    return find
        return False

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

        if (place.is_controller):
            args["text"] = ''
            self.window.run_command("show_overlay", args)
            self.window.run_command("insert", {
                "characters": place.path
            })
        else:

            if (place.find):
                view = self.window.open_file(place.path)
                self.find_location(view, place.find)
            else:
                self.window.run_command("show_overlay", args)
        return

    def find_location(self, view, find):
        if view.is_loading():
            sublime.set_timeout(lambda: self.find_location(view, find), 50)
            return

        if (isinstance(find, str)):
            view = self.window.active_view()
            location = view.find(find, 0)
            # fix .env not show selected if no scrolling happened
            view.set_viewport_position((0, 1))
            view.sel().clear()
            view.sel().add(location)
            view.show(location)
