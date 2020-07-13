import sublime
import sublime_plugin
from re import compile
from os.path import basename

plugin_settings = None
user_settings = None
extensions = None
place = None
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

path_helper_pattern = compile(r"([^_]+)_path\(\s*(['\"])([^'\"]*)\2")

find_pattern = "(['\"]{1})%s\\1\\s*=>"


class Place:
    is_controller = False

    def __init__(self, path, location=None):
        self.path = path
        self.location = location


class GotoLocation(sublime_plugin.EventListener):
    def on_activated(self, view):
        global place
        filepath = view.file_name()
        if (not place or not filepath):
            return
        if (basename(filepath) != basename(place.path)):
            return
        if (not isinstance(place.location, str)):
            return

        location = view.find(place.location, 0)
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

        places = (
            self.path_helper_place,
            self.controller_place,
            self.static_file_place,
            self.env_place,
            self.config_place,
            self.lang_place,
        )

        for fn in places:
            place = fn(path, line, selected)
            if place:
                return place

        return self.view_place(path, line, selected)

    def controller_place(self, path, line, selected):
        find = "@" in path or "Controller" in path
        if find is False:
            return False
        path = path.replace('@', '.php@')
        # it's not absolute path namespace
        if '\\' != path[0]:
            namespace = self._namespace.find(self.view, selected)
            if namespace:
                path = namespace + '\\' + path
        place = Place(path)
        place.is_controller = True
        return place

    def config_place(self, path, line, selected):
        for pattern in config_patterns:
            matcheds = pattern.finditer(line)
            for matched in matcheds:
                if (matched and path == matched.group(2)):
                    split = path.split('.')
                    path = 'config/' + split[0] + '.php'
                    location = None
                    if (2 <= len(split)):
                        location = find_pattern % (split[1])
                    return Place(path, location)

        return False

    def lang_place(self, path, line, selected):
        for pattern in lang_patterns:
            matched = pattern.search(line)
            if (matched and path == matched.group(2)):
                split = path.split(':')
                vendor = ''
                # it's package trans
                if (3 == len(split)):
                    vendor = '/vendor/' + split[0]
                keys = split[-1].split('.')
                path = 'resources/lang' + vendor + '/' + keys[0] + '.php'

                location = None
                if (2 <= len(keys)):
                    location = find_pattern % (keys[1])
                return Place(path, location)

        return False

    def static_file_place(self, path, line, selected):
        find = (path.split('.')[-1].lower() in extensions)
        if find is False:
            return False

        # remove dot symbols
        split = list(filter(
            lambda x: x != '..' and x != '.',
            path.split('/')))
        return Place('/'.join(split))

    def env_place(self, path, line, selected):
        matched = env_pattern.search(line)
        find = (matched and path == matched.group(2))
        if find:
            return Place('.env', path)
        return False

    def view_place(self, path, line, selected):
        split = path.split(':')
        vendor = ''
        # vendor or namespace
        if (3 == len(split)):
            # vendor probably is lowercase
            if (split[0] == split[0].lower()):
                vendor = split[0] + '/'

        path = split[-1]
        path = vendor + path.replace('.', '/') + '.blade.php'
        return Place(path)

    def path_helper_place(self, path, line, selected):
        matched = path_helper_pattern.search(line)
        if (matched and path == matched.group(3)):
            prefix = matched.group(1) + '/'
            if 'base/' == prefix:
                prefix = ''
            elif 'resource/' == prefix:
                prefix = 'resources/'

            return Place(prefix + path)
        return False

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
