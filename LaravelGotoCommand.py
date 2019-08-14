import sublime
import sublime_plugin


plugin_settings = None
user_settings = None
extensions = None


class LaravelGotoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        globals()['plugin_settings'] = sublime\
            .load_settings("Plugin.sublime-settings")
        globals()['user_settings'] = sublime.\
            load_settings("Preferences.sublime-settings")
        extensions = user_settings.get("static_extensions", []) +\
            plugin_settings.get("static_extensions")
        globals()['extensions'] = list(map(lambda ext: '.' + ext, extensions))

    def run(self, edit):
        self.window = sublime.active_window()
        if (len(self.window.folders()) == 0):
            return

        path = self.get_path(self.view.sel()[0])
        # print(path)
        if path:
            self.search(path)
        return

    def substr(self, mixed):
        return self.view.substr(mixed)

    def get_path(self, selected):
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

        is_controller = "@" in path or "Controller" in path
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
        return (path[-3:] in extensions)
