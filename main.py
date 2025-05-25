import sys
import sublime
import sublime_plugin
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
from .lib.finder import get_place
from .lib.setting import Setting
from .lib.router import Router

place = None


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


class GotoControllerCommand(sublime_plugin.WindowCommand):
    uris = []

    def run(self):
        router = Router()
        self.uris = router.uris()
        items = []
        for uri in self.uris:
            item = sublime.QuickPanelItem(uri.label, uri.detail)
            items.append(item)

        self.window.show_quick_panel(
            items,
            self.on_done,
            sublime.MONOSPACE_FONT
        )

    def on_done(self, index):
        if index == -1:
            return  # User cancelled the selection

        uri = self.uris[index]
        goto_place(uri.place)


class GotoLocation(sublime_plugin.EventListener):
    def on_load(self, view):
        global place
        filepath = view.file_name()
        if (not place or not filepath):
            place = None
            return
        if (basename(filepath) != basename(place.path)):
            found = False
            for path in place.paths:
                if filepath.endswith(path):
                    found = True
                    break
            if not found:
                place = None
                return
        if (not isinstance(place.location, str)):
            place = None
            return
        spot_location(view, place, filepath)

    def on_post_save_async(self, view):
        Router().update(view.file_name())

    def on_hover(self, view, point, hover_zone):
        if view.is_popup_visible():
            return
        if sublime.HOVER_TEXT != hover_zone:
            return
        if not Setting().get('show_hover'):
            return
        global place
        selection = Selection(view, point)
        place = get_place(selection)

        if place and place.path:
            content = self.build_link(place.path)

            if place.paths:
                content = '<br/>'.join(map(self.build_link, place.paths))
            if place.uris:
                content += '<br/><br/>' +\
                    self.build_link(
                        'Open all files above in new window',
                        'A!!'
                    )

            view.show_popup(
                content,
                flags=sublime.HIDE_ON_MOUSE_MOVE_AWAY,
                location=point,
                max_width=640,
                on_navigate=self.on_navigate
            )

    def build_link(self, path, href=None):
        if not href:
            href = path

        return '<a href="' + href + '">' + path + '</a>'

    def on_navigate(self, link):
        global place

        if link == 'A!!' and place.uris:
            open_file_layouts(place.uris)
            return
        if place.paths and link in place.paths:
            place.path = link
            place.paths = []

        goto_place(place)


def goto_place(place):
    if place is None:
        sublime.status_message('Laravel Goto: unidentified string.')
        return

    window = sublime.active_window()

    if place.paths:
        if place.uris:
            place.paths.append('Open all files above in new window')
        window.show_quick_panel(
            place.paths,
            on_path_select
            )
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
    if -1 == idx:
        return

    if place.uris and place.paths[idx] == place.paths[-1]:
        open_file_layouts(place.uris)
        return

    place.path = place.paths[idx]
    place.paths = []
    goto_place(place)


def open_file_layouts(files=[]):
    '''open files in multi-columns layouts'''
    width = 1 / len(files)
    cols = [0.0]
    cells = []
    for (idx, file) in enumerate(files):
        cols.append(width*idx+width)
        cells.append([idx, 0, idx+1, 1])

    active_window = sublime.active_window()
    active_window.run_command('new_window')
    new_window = sublime.active_window()
    new_window.set_layout({
        "cols": cols,
        "rows": [0.0, 1.0],
        "cells": cells
    })
    for (idx, file) in enumerate(files):
        new_window.open_file(file)
        new_window.set_view_index(new_window.active_view(), idx, 0)
    return


def spot_location(view, place, filepath):
    ''' spot place location on view '''
    if not place.location:
        return

    location = place.location
    filename = basename(filepath)
    # print(filename)
    if filename in place.locations:
        location = place.locations[filename]

    found = view.find(location, 0)
    # fix .env not showing selected if no scrolling happened
    view.set_viewport_position((0, 1))
    view.sel().clear()
    view.sel().add(found)
    view.show(found)
