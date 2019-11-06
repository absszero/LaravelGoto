import sublime
import sublime_plugin
from re import compile
from os.path import basename

plugin_settings = None
user_settings = None
extensions = None
place = None
patterns = [
    compile(r"namespace\s*\(\s*(['\"])\s*([^'\"]+)\1"),
    compile(r"['\"]namespace['\"]\s*=>\s*(['\"])([^'\"]+)\1"),
]
config_patterns = [
    compile(r"Config::[^'\"]*(['\"])([^'\"]*)\1"),
    compile(r"config\([^'\"]*(['\"])([^'\"]*)\1"),
]
lang_patterns = [
    compile(r"__\([^'\"]*(['\"])([^'\"]*)\1"),
    compile(r"@lang\([^'\"]*(['\"])([^'\"]*)\1"),
    compile(r"trans\([^'\"]*(['\"])([^'\"]*)\1"),
    compile(r"trans_choice\([^'\"]*(['\"])([^'\"]*)\1"),
]

env_pattern = compile(r"env\(\s*(['\"])([^'\"]*)\1")

excludes_dir = ['.git', '.svn', 'node_modules', 'vendor']

find_pattern = "(['\"]{1})%s\\1\\s*=>"


class Place:
    def __init__(self, path, is_controller, find):
        self.path = path
        self.is_controller = is_controller
        self.find = find


class GotoLocation(sublime_plugin.EventListener):
    def on_activated(self, view):
        global place
        filepath = view.file_name()
        if (not place or not filepath):
            return
        if (basename(filepath) != basename(place.path)):
            return
        if (not isinstance(place.find, str)):
            return

        location = view.find(place.find, 0)
        # fix .env not show selected if no scrolling happened
        view.set_viewport_position((0, 1))
        view.sel().clear()
        view.sel().add(location)
        view.show(location)
        place = None


class Namespace:
    def __init__(self):
        self._patterns = [
            compile(r"namespace\s*\(\s*(['\"])\s*([^'\"]+)\1"),
            compile(r"['\"]namespace['\"]\s*=>\s*(['\"])([^'\"]+)\1"),
        ]

    def find(self, view, selection):
        ''' find the namespace of the selection'''
        self._fullText = view.substr(sublime.Region(0, view.size()))
        self._length = len(self._fullText)

        blocks = self.blocks(selection)
        for closure in blocks:
            if closure['range'].contains(selection):
                return closure['namespace']
        return ''

    def blocks(self, selection):
        '''get all closure blocks'''
        blocks = []
        for pattern in self._patterns:
            for match in pattern.finditer(self._fullText):
                start = match.start()
                if selection.a > start:
                    end = self.getEndPosition(start)
                    blocks.append({
                        'namespace': match.group(2),
                        'range': sublime.Region(start, end)
                    })
        return blocks

    def getEndPosition(self, start):
        '''get the end position from the start position'''
        result = []
        while self._length > start:
            if ('{' == self._fullText[start]):
                result.append(start)
            elif ('}' == self._fullText[start]):
                result.pop()
                if (0 == len(result)):
                    return start
            start = start + 1

        return start


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
        self._namespace = Namespace()

    def run(self, edit):
        global place
        self.window = sublime.active_window()
        selection = self.get_selection(self.view.sel()[0])
        place = self.get_place(selection)
        self.search(place)
        return

    def is_visible(self):
        filename = self.view.file_name()
        return bool(filename and filename.endswith('.php'))

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
                namespace = self._namespace.find(self.view, selected)
                if namespace:
                    path = namespace + '\\' + path

        elif(self.is_static_file(path)):
            # remove dot symbols
            split = list(filter(
                lambda x: x != '..' and x != '.',
                path.split('/')))
            path = '/'.join(split)
            pass

        elif(self.is_env(path, line)):
            find = path
            path = '.env'

        elif(self.is_config(path, line)):
            split = path.split('.')
            path = 'config/' + split[0] + '.php'
            if (2 <= len(split)):
                find = find_pattern % (split[1])

        elif(self.is_lang(path, line)):
            # a package lang file
            if '::' in path:
                path = path.split(':')[-1] + '.php'
            else:
                split = path.split('.')
                path = 'resources/lang/' + split[0] + '.php'
                if (2 <= len(split)):
                    find = find_pattern % (split[1])

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
            self.window.run_command("show_overlay", args)
        return
