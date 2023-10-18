import sys
import sublime
import sublime_plugin
from re import compile
from os.path import basename
from typing import Optional

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
from .lib.finder import get_place, init_extensions

place = None
currentSettings = None  # type:Optional[sublime.Settings]


class GotoLocation(sublime_plugin.EventListener):
    def on_activated(self, view):
        init_extensions()
        global place
        filepath = view.file_name()
        if (not place or not filepath):
            return
        if (basename(filepath) != basename(place.path)):
            return
        if (not isinstance(place.location, str)):
            return

        location = view.find(place.location, 0)
        # fix .env not showing selected if no scrolling happened
        view.set_viewport_position((0, 1))
        view.sel().clear()
        view.sel().add(location)
        view.show(location)
        place = None

    def on_hover(self, view, point, hover_zone):
        if view.is_popup_visible():
            return
        if sublime.HOVER_TEXT != hover_zone:
            return
        if not currentSettings or not currentSettings.get('show_hover'):
            return
        global place
        selection = Selection(view, point)
        place = get_place(selection)

        if place and place.path:
            content = self.build_link(place.path)

            if place.paths:
                content = '<br/>'.join(map(self.build_link, place.paths))

            view.show_popup(
                content,
                flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                location=point,
                max_width=640,
                on_navigate=self.on_navigate
            )

    def build_link(self, path):
        return '<a href="' + path + '">' + path + '</a>'

    def on_navigate(self, link):
        global place
        if place.paths and link in place.paths:
            place.path = link
            place.paths = []

        goto_place(place)


class LaravelGotoCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        super().__init__(view)

    def run(self, edit):
        global place
        selection = Selection(self.view)
        place = get_place(selection)
        goto_place(place)

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


def goto_place(place):
    if place is None:
        sublime.status_message('Laravel Goto: unidentified string.')
        return

    window = sublime.active_window()

    if place.paths:
        window.show_quick_panel(place.paths, on_path_select, placeholder="Select a component file")
        return

    if place.uri:
        window.open_file(place.uri)
        return

    args = {
        "overlay": "goto",
        "show_files": True,
        "text": place.path
    }

    if place.is_controller:
        args["text"] = ''
        window.run_command("show_overlay", args)
        window.run_command("insert", {
            "characters": place.path
        })
        return

    window.run_command("show_overlay", args)


def on_path_select(idx):
    if -1 is idx:
        return
    place.path = place.paths[idx]
    place.paths = []
    goto_place(place)


def plugin_loaded():
    global currentSettings
    currentSettings = sublime.load_settings('LaravelGoto.sublime-settings')
