import sys
import sublime
import sublime_plugin
from re import compile
from os.path import basename

if int(sublime.version()) >= 3114:

    # Clear module cache to force reloading all modules of this package.
    # See https://github.com/emmetio/sublime-text-plugin/issues/35
    prefix = __package__ + "."  # don't clear the base package
    for module_name in [
        module_name
        for module_name in sys.modules
        if module_name.startswith(prefix) and module_name != __name__
    ]:
        del sys.modules[module_name]
    prefix = None

from .lib.selection import Selection
from .lib.place import get_place, init_extensions

place = None


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


class LaravelGotoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)
        init_extensions()

    def run(self, edit):
        global place
        self.window = sublime.active_window()
        selection = Selection(self.view)
        place = get_place(selection)
        self.search(place)
        return

    def is_visible(self):
        filename = self.view.file_name()
        return bool(filename and (
                filename.endswith('.php') or
                filename.endswith('.js') or
                filename.endswith('.ts') or
                filename.endswith('.jsx') or
                filename.endswith('.vue')
                )
            )

    def search(self, place):
        if place is None:
            sublime.status_message('No matched filename.')
            return

        args = {
            "overlay": "goto",
            "show_files": True,
            "text": place.path
        }

        if place.is_controller:
            args["text"] = ''
            self.window.run_command("show_overlay", args)
            self.window.run_command("insert", {
                "characters": place.path
            })
        else:
            self.window.run_command("show_overlay", args)
        return
