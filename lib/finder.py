from re import compile
from .namespace import Namespace
from .place import Place
from .middleware import Middleware
from .console import Console
from .router import Router
from .language import Language
from .setting import Setting


find_pattern = """(['"]{1})%s\\1\\s*=>"""


def get_place(selection):
    line = selection.get_line()
    lines = selection.get_lines_after_delimiter()

    path = selection.get_path()

    places = (
        path_helper_place,
        static_file_place,
        env_place,
        config_place,
        filesystem_place,
        lang_place,
        blade_place,
        inertiajs_place,
        livewire_place,
        component_place,
        middleware_place,
        command_place,
        route_place,
        controller_place,
    )

    for fn in places:
        place = fn(path, line, lines, selection)
        if place:
            return place


def set_controller_action(path, selected, blocks):
    ''' set the controller action '''

    class_controller_pattern = compile(r"""(.+)\.php\s*,\s*["']{1}(.+)""")
    path = path.replace('@', '.php@')
    path = path.replace('::class', '.php')
    if selected.is_class:
        matched = class_controller_pattern.search(path)
        if matched:
            path = matched.group(1) + '.php@' + matched.group(2)

    elif len(blocks) and blocks[0]['is_namespace'] is False:
        """resource or controller route"""
        new_path = blocks[0]['namespace']
        if new_path != path:
            path = new_path + '.php@' + path
        else:
            path = new_path + '.php'

    return path


def set_controller_namespace(path, selected, ns):
    ''' set the controller namespace '''

    if '\\' != path[0] and ns:
        # it's not absolute path namespace, get group namespace
        path = ns + '\\' + path.lstrip('\\')

    return path


def controller_place(path, line, lines, selected):
    namespace = Namespace(selected.view)
    blocks = namespace.get_blocks(selected)
    is_controller = "Controller" in path or selected.is_class

    if is_controller is False and 0 == len(blocks):
        return False

    path = set_controller_action(path, selected, blocks)

    ns = namespace.find(blocks)
    path = set_controller_namespace(path, selected, ns)

    place = Place(path)
    place.is_controller = True
    return place


def config_place(path, line, lines, selected):
    config_patterns = [
        compile(r"""Config::[^'"]*(['"])([^'"]*)\1"""),
        compile(r"""config\([^'"]*(['"])([^'"]*)\1"""),
    ]
    for pattern in config_patterns:
        matched = pattern.search(line) or pattern.search(lines)
        if (matched and path == matched.group(2)):
            split = path.split('.')
            path = 'config/' + split[0] + '.php'
            location = None
            if (2 <= len(split)):
                location = find_pattern % (split[1])
            return Place(path, location)

    return False


def filesystem_place(path, line, lines, selected):
    pattern = compile(r"""Storage::disk\(\s*['"]([^'"]+)""")
    matched = pattern.search(line) or pattern.search(lines)
    if (matched and path == matched.group(1)):
        path = 'config/filesystems.php'
        location = "(['\"]{1})" + matched.group(1) + "\\1\\s*=>"
        return Place(path, location)

    return False


def inertiajs_place(path, line, lines, selected):
    inertiajs_patterns = [
        compile(r"""Route::inertia\s*\([^,]+,\s*['"]([^'"]+)"""),
        compile(r"""Inertia::render\s*\(\s*['"]([^'"]+)"""),
        compile(r"""inertia\s*\(\s*['"]([^'"]+)"""),
    ]
    for pattern in inertiajs_patterns:
        matched = pattern.search(line) or pattern.search(lines)
        if (matched and matched.group(1) in path):
            return Place(matched.group(1))

    return False


def livewire_place(path, line, lines, selected):
    livewire_patterns = [
        compile(r"""livewire:([^\s"'>]+)"""),
        compile(r"""@livewire\s*\(\s*['"]([^'"]+)"""),
    ]
    for pattern in livewire_patterns:
        matched = pattern.search(line) or pattern.search(lines)
        if matched:
            path = camel_case(matched.group(1))
            path = path.replace('.', '/') + '.php'
            return Place(path)

    return False


def camel_case(snake_str):
    components = snake_str.split('-')
    return components[0].title() + ''.join(x.title() for x in components[1:])


def lang_place(path, line, lines, selected):
    lang_patterns = [
        compile(r"""__\([^'"]*(['"])([^'"]*)\1"""),
        compile(r"""@lang\([^'"]*(['"])([^'"]*)\1"""),
        compile(r"""trans\([^'"]*(['"])([^'"]*)\1"""),
        compile(r"""trans_choice\([^'"]*(['"])([^'"]*)\1"""),
    ]

    language = None
    for pattern in lang_patterns:
        matched = pattern.search(line) or pattern.search(lines)
        if (not matched or path != matched.group(2)):
            continue

        if not language:
            language = Language()
        place = language.get_place(path)
        return place

    return False


def static_file_place(path, line, lines, selected):
    find = (path.split('.')[-1].lower() in Setting().exts())
    if find is False:
        return False

    # remove dot symbols
    split = list(filter(
        lambda x: x != '..' and x != '.',
        path.split('/')))
    return Place('/'.join(split))


def env_place(path, line, lines, selected):
    env_pattern = compile(r"""env\(\s*(['"])([^'"]*)\1""")
    matched = env_pattern.search(line) or env_pattern.search(lines)
    find = (matched and path == matched.group(2))
    if find:
        return Place('.env', path)
    return False


def component_place(path, line, lines, selected):
    component_pattern = compile(r"""<\/?x-([^\/\s>]*)""")
    matched = component_pattern.search(line) or component_pattern.search(lines)
    if matched is None:
        return False

    path = matched.group(1).strip()

    split = path.split(':')
    vendor = 'View/Components/'
    res_vendor = 'views/components/'
    # vendor or namespace
    if (3 == len(split)):
        # vendor probably is lowercase
        if (split[0] == split[0].lower()):
            vendor = split[0] + '/'
            res_vendor = split[0] + '/'

    sections = split[-1].split('.')
    place = Place(res_vendor + '/'.join(sections) + '.blade.php')
    place.paths.append(place.path)

    for i, s in enumerate(sections):
        sections[i] = s.capitalize()
    sections[-1] = camel_case(sections[-1])
    place.paths.append(vendor + '/'.join(sections) + '.php')

    return place


def transform_blade(path):
    split = path.split(':')
    vendor = ''
    # vendor or namespace
    if (3 == len(split)):
        # vendor probably is lowercase
        if (split[0] == split[0].lower()):
            vendor = split[0] + '/'

    path = split[-1]
    path = vendor + path.replace('.', '/')
    if path.endswith('/blade/php'):
        path = path[:-1*len('/blade/php')]

    path += '.blade.php'
    return path


def blade_place(path, line, lines, selected):
    blade_patterns = [
        compile(r"""view\(\s*(['"])([^'"]*)\1"""),
        compile(r"""[lL]ayout\(\s*(['"])([^'"]*)\1"""),
        compile(r"""View::exists\(\s*(['"])([^'"]*)\1"""),
        compile(r"""View::composer\(\s*(['"])([^'"]*)\1"""),
        compile(r"""View::creator\(\s*(['"])([^'"]*)\1"""),
        compile(r"""\$view\s*=\s*(['"])([^'"]*)\1"""),
        compile(r"""view:\s*(['"])([^'"]*)\1"""),
        compile(r"""view\(\s*['"][^'"]*['"],\s*(['"])([^'"]*)\1"""),
        compile(r"""['"]layout['"]\s*=>\s*(['"])([^'"]*)\1"""),
        compile(r"""@include(If\b)?\(\s*(['"])([^'"]*)\2"""),
        compile(r"""@extends\(\s*(['"])([^'"]*)\1"""),
        compile(r"""@include(When|Unless\b)?\([^'"]+(['"])([^'"]+)"""),
        compile(r"""(resources\/views[^\s'"-]+)"""),
    ]
    for pattern in blade_patterns:
        matched = pattern.search(line) or pattern.search(lines)
        if matched is None:
            continue

        groups = matched.groups()
        if path == groups[-1]:
            path = groups[-1].strip()
            path = transform_blade(path)
            return Place(path)

    multi_views_patterns = [
        compile(r"""@includeFirst\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""),
        compile(r"""View::composer\(\[(\s*['"][^'"]+['"]\s*[,]?\s*){2,}\]"""),
        compile(r"""@each\(['"][^'"]+['"]\s*,[^,]+,[^,]+,[^)]+"""),
        compile(r"""View::first[^'"]*(['"])([^'"]*)\1"""),
    ]
    for pattern in multi_views_patterns:
        if pattern.search(line) or pattern.search(lines):
            path = transform_blade(path)
            return Place(path)

    return False


def path_helper_place(path, line, lines, selected):
    path_helper_pattern = compile(r"""([\w^_]+)_path\(\s*(['"])([^'"]*)\2""")
    matched = path_helper_pattern.search(line) or\
        path_helper_pattern.search(lines)
    if (matched and path == matched.group(3)):
        prefix = matched.group(1) + '/'
        if 'base/' == prefix:
            prefix = ''
        elif 'resource/' == prefix:
            prefix = 'resources/'

        return Place(prefix + path)
    return False


def middleware_place(path, line, lines, selected):
    middleware_patterns = [
        compile(r"""[m|M]iddleware\(\s*\[?\s*(['"][^'"]+['"]\s*,?\s*)+"""),
        compile(r"""['"]middleware['"]\s*=>\s*\s*\[?\s*(['"][^'"]+['"]\s*,?\s*){1,}\]?"""),  # noqa: E501
    ]
    middlewares = None
    for pattern in middleware_patterns:
        matched = pattern.search(line) or pattern.search(lines)
        if not matched:
            continue

        if not middlewares:
            middleware = Middleware()
            middlewares = middleware.all()

        # remove middleware parameters
        alias = path.split(':')[0]
        place = middlewares.get(alias)
        if place:
            return place


def command_place(path, line, lines, selected):
    patterns = [
        compile(r"""Artisan::call\(\s*['"]([^\s'"]+)"""),
        compile(r"""command\(\s*['"]([^\s'"]+)"""),
    ]

    commands = None
    for pattern in patterns:
        match = pattern.search(line) or pattern.search(lines)
        if not match:
            continue

        if not commands:
            console = Console()
            commands = console.all()

        signature = match.group(1)
        place = commands.get(signature)
        if place:
            return place

        return place


def route_place(path, line, lines, selected):
    patterns = [
        compile(r"""route\(\s*['"]([^'"]+)"""),
        compile(r"""['"]route['"]\s*=>\s*(['"])([^'"]+)"""),
    ]

    routes = None
    for pattern in patterns:
        match = pattern.search(line) or pattern.search(lines)
        if not match:
            continue

        if not routes:
            router = Router()
            routes = router.all()

        place = routes.get(match.group(1))
        if place:
            return place

        return place
