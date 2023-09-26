import sublime

from unittest.mock import patch
from . import unittest

from LaravelGoto.lib.selection import Selection
from LaravelGoto.lib.finder import get_place

class TestFinder(unittest.ViewTestCase):
    def test_controller_route(self):
        self.fixture("""
        Route::group(['namespace' => 'Resource'], function () {
            Route::controller('HelloController')->group(function () {
                Route::get('/posts/{id}', 'sh|ow');
            });
        });""")
        place = self.assertPath("Resource\\HelloController.php@show")
        self.assertEqual(True, place.is_controller)

    def test_resource_route(self):
        self.fixture("""
        Route::group(['namespace' => 'Resource'], function () {
            Route::resource('photo', 'Hello|Controller', ['only' => [
                'index', 'show'
            ]]);
        });""")
        place = self.assertPath("Resource\\HelloController.php")
        self.assertEqual(True, place.is_controller)


    def test_resource_route_action(self):
        self.fixture("""
        Route::group(['namespace' => 'Resource'], function () {
            Route::resource('photo', 'HelloController', ['only' => [
                'index', 'sho|w'
            ]]);
        });""")
        place = self.assertPath("Resource\\HelloController.php@show")
        self.assertEqual(True, place.is_controller)

    def test_controller(self):
        self.fixture("""Route::get('/', 'HelloControll|er@index');""")
        place = self.assertPath("HelloController.php@index")
        self.assertEqual(True, place.is_controller)

    def test_component(self):
        self.fixture("""<x-form.|input/>""")
        self.assertPath("form/input.php")

    def test_closing_tag_component(self):
        self.fixture("""</x-al|ert>""")
        self.assertPath("alert.php")

    def test_component_with_namespace(self):
        self.fixture("""<x-namespace::|alert/>""")
        self.assertPath("namespace/alert.php")

    def test_view(self):
        self.fixture("""
        Route::get('/', function () {
            return view('hello|_view');
        });""")
        self.assertPath("hello_view.blade.php")

    def test_layout_method(self):
        self.fixture("""layout('hello|_view');""")
        self.assertPath("hello_view.blade.php")

    def test_view_var(self):
        self.fixture("""$view = 'hello|_view'""")
        self.assertPath("hello_view.blade.php")

    def test_view_in_mailble(self):
        self.fixture("""view: 'ema|ils.test',""")
        self.assertPath("emails/test.blade.php")

    def test_view_in_route_view(self):
        self.fixture("""Route::view('/welcome', 'pages.wel|come', ['name' => 'Taylor']);""")
        self.assertPath("pages/welcome.blade.php")

    def test_view_in_config_livewire_php(self):
        self.fixture("""'layout' => 'layou|ts.app',""")
        self.assertPath("layouts/app.blade.php")

    def test_blade_include_and_includeIf(self):
        self.fixture("""@includeIf('view.na|me', ['status' => 'complete'])""")
        self.assertPath("view/name.blade.php")

    def test_blade_extends(self):
        self.fixture("""@extends('view.na|me')""")
        self.assertPath("view/name.blade.php")

    def test_blade_inclcudeUnless_and_inclcudeWhen(self):
        self.fixture("""@includeUnless($boolean, 'view|.name', ['status' => 'complete'])""")
        self.assertPath("view/name.blade.php")

    def test_blade_includeFirst(self):
        self.fixture("""@includeFirst(['custom.admin', 'ad|min'], ['status' => 'complete'])""")
        self.assertPath("admin.blade.php")

    def test_blade_each(self):
        self.fixture("""@each('view.name', $jobs, 'job', 'view|.empty')""")
        self.assertPath("view/empty.blade.php")

    def test_blade_comment(self):
        self.fixture("""'{{-- resources/views/comp|onents/layout --}}'""")
        self.assertPath('resources/views/components/layout.blade.php')

    def test_full_blade_path(self):
        self.fixture("""'resources/views/comp|onents/layout.blade.php'""")
        self.assertPath('resources/views/components/layout.blade.php')


    def test_staticFile(self):
        self.fixture("""'hello|.JS';""")
        self.assertPath("hello.JS")

    def test_namespace58(self):
        self.fixture("""
        Route::namespace('58')->group(function () {
            Route::get('/', 'FiveEightC|ontroller@index');
        });""")
        place = self.assertPath('58\\FiveEightController.php@index')
        self.assertEqual(True, place.is_controller)

    def test_namespace52(self):
        self.fixture("""
        Route::group(['namespace' => '52'], function () {
            Route::get('/', 'FiveTw|oController@index');
        });""")
        place = self.assertPath('52\\FiveTwoController.php@index')
        self.assertEqual(True, place.is_controller)

    def test_namespaceLumen(self):
        self.fixture("""
        $router->group(['namespace' => 'Lumen'], function () use ($router) {
            Route::get('/', 'LumenCo|ntroller@index');
        });""")

        place = self.assertPath('Lumen\\LumenController.php@index')
        self.assertEqual(True, place.is_controller)

    def test_view_namespace(self):
        self.fixture("""
        Route::get('/', function () {
            return view('Namespace::h|ello_view');
        });""")
        self.assertPath('hello_view.blade.php')

    def test_absolute_path(self):
        self.fixture("""
        Route::group(['namespace' => 'Abc'], function () {
            Route::get('/', '\\Absolute\\IndexCont|roller@index')->name('index');
        });""")
        place = self.assertPath('\\Absolute\\IndexController.php@index')
        self.assertEqual(True, place.is_controller)

    def test_facade_config_get(self):
        self.fixture("""Config::get('app.ti|mezone');""")
        place = self.assertPath('config/app.php')
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_facade_config_set(self):
        self.fixture("""Config::set(   'app.timez|one', 'UTC');""")
        place = self.assertPath('config/app.php')
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_config_get_only_file(self):
        self.fixture("""config('a|pp');""")
        self.assertPath('config/app.php')

    def test_config_get_helper(self):
        self.fixture("""config('app.timez|one');""")
        place = self.assertPath('config/app.php')
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_config_set_helper(self):
        self.fixture("""config(     ['app.timez|one' => 'UTC']);""")
        place = self.assertPath('config/app.php')
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_env(self):
        self.fixture("""env(   'APP|_DEBUG', false);""")
        place = self.assertPath('.env')
        self.assertEqual('APP_DEBUG', place.location)

    def test_lang_underscore(self):
        self.fixture("""__('messages.w|elcome');""")
        self.assertPath('lang/messages.php')

    def test_lang_blade_directive(self):
        self.fixture("""@lang('messages.we|lcome');""")
        self.assertPath('lang/messages.php')

    def test_lang_trans(self):
        self.fixture("""trans('messages.we|lcome');""")
        self.assertPath('lang/messages.php')

    def test_lang_trans_choice(self):
        self.fixture("""trans_choice('messages.a|pples', 10);""")
        self.assertPath('lang/messages.php')

    def test_lang_trans_package(self):
        self.fixture("""trans('package::messa|ges');""")
        self.assertPath('lang/vendor/package/messages.php')

    def test_relative_path_static_file(self):
        self.fixture("""'./../../hel|lo.css'""")
        self.assertPath('hello.css')

    def test_package_view(self):
        self.fixture("""view('package::hell|o_view');""")
        self.assertPath('package/hello_view.blade.php')

    def test_view_first(self):
        self.fixture("""View::first(['custom|.admin', 'admin'], $data);""")
        self.assertPath('custom/admin.blade.php')
        self.fixture("""View::first(['custom.admin', 'ad|min'], $data);""")
        self.assertPath('admin.blade.php')

    def test_view_composer(self):
        self.fixture("""View::composer(['pro|file', 'dashboard'], MultiComposer::class);""")
        self.assertPath('profile.blade.php')

        self.fixture("""View::composer(['profile', 'das|hboard'], MultiComposer::class);""")
        self.assertPath('dashboard.blade.php')

        self.fixture("""View::composer('prof|ile', ProfileComposer::class);""")
        self.assertPath('profile.blade.php')

    def test_view_creator(self):
        self.fixture("""View::creator('prof|ile', ProfileComposer::class);""")
        self.assertPath('profile.blade.php')

    def test_view_resource_string(self):
        self.fixture("""'resources/views/pages/public/cha|rge'""")
        self.assertPath('resources/views/pages/public/charge.blade.php')

    def test_view_exists(self):
        self.fixture("""View::exists('emails.c|ustomer');""")
        self.assertPath('emails/customer.blade.php')

    def test_app_path(self):
        self.fixture("""app_path('Us|er.php');""")
        self.assertPath('app/User.php')

    def test_config_path(self):
        self.fixture("""config_path('ap|p.php');""")
        self.assertPath('config/app.php')

    def test_database_path(self):
        self.fixture("""database_path('UserFacto|ry.php');""")
        self.assertPath('database/UserFactory.php')

    def test_public_path(self):
        self.fixture("""public_path('css/ap|p.css');""")
        self.assertPath('public/css/app.css')

    def test_resource_path(self):
        self.fixture("""resource_path('sass/ap|p.scss');""")
        self.assertPath('resources/sass/app.scss')

    def test_storage_path(self):
        self.fixture("""storage_path('logs/lara|vel.log');""")
        self.assertPath('storage/logs/laravel.log')

    def test_double_brackets_path(self):
        self.fixture("""realpath(storage_path('logs/lar|avel.log'));""")
        self.assertPath('storage/logs/laravel.log')

    def test_v8_namespace_route(self):
        self.fixture("""Route::get('/', [L8\\EightContro|ller::class, 'index']);""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual('L8\\EightController.php@index', place.path)

    def test_v8_route(self):
        self.fixture("""Route::get('/', EightContro|ller::class);""")
        self.assertPath('EightController.php')

    def test_v8_group_namespae_abs_route(self):
        self.fixture("""
        Route::group(['namespace' => 'L8'], function () {
            Route::get('/', [\\EightControl|ler::class, 'index']);
        });""")
        self.assertPath('\\EightController.php@index')

    def test_v8_group_namespae_route(self):
        self.fixture("""
        Route::group(['namespace' => 'L8'], function () {
            Route::get('/', [EightCon|troller::class, 'index']);
        });""")

        selection = Selection(self.view)
        place = get_place(selection)
        self.assertEqual(True, place.is_controller)
        self.assertEqual('L8\\EightController.php@index', place.path)

    def test_inertiajs_function(self):
        self.fixture("""inertia("About/AboutCo|mponent");""")
        self.assertPath("About/AboutComponent")

    def test_inertiajs_render(self):
        self.fixture("""Inertia::render("About/AboutC|omponent");""")
        self.assertPath("About/AboutComponent")

    def test_inertiajs_route(self):
        self.fixture("""Route::inertia("/about", "About/AboutCom|ponent");""")
        self.assertPath("About/AboutComponent")

    def test_livewire_tag(self):
        self.fixture("""<livewire:nav.sho|w-post />""")
        self.assertPath("Nav/ShowPost.php")

    def test_livewire_blade_directive(self):
        self.fixture("""@livewire("nav.show|-post")""")
        self.assertPath("Nav/ShowPost.php")

    def test_multiline(self):
        examples = {
            'layouts/app.blade.php':
            """layout(
                'lay|outs.app'
            )""",
            'About/AboutComponent':
            """inertia(
                'About/AboutCo|mponent'
            );""",
            'hello_view.blade.php':
            """view(
                'hello|_view', ['name' => 'James']
            );""",
            'HelloController.php@index':
            """Route::get(
                '/', 'HelloControlle|r@index'
            );""",
            'config/app.php':
            """Config::get(
                'app.t|imezone'
            );""",
            '.env':
            """env(
                'APP_DEB|UG'
                , false
            );""",
            'lang/messages.php':
            """__(
                'messages.|welcome'
            );""",
            'app/User.php':
            """app_path(
                'Use|r.php'
            );"""
        }

        for expected, content in examples.items():
            self.fixture(content)
            self.assertPath(expected, expected)

    @patch('LaravelGoto.lib.workspace.get_folders')
    @patch('LaravelGoto.lib.workspace.get_file_content')
    def test_middleware(self, mock_get_file_content, mock_get_folders):
        mock_get_file_content.return_value = self.get_kernel()
        mock_get_folders.return_value = [self.get_test_dir()]
        self.fixture("""Route::middleware(['web:1234', 'auth|:abc']);""")
        selection = Selection(self.view)
        place = get_place(selection)
        self.assertEqual("App/Http/Middleware/Authenticate.php", place.path)

        self.fixture("""Route::group(['middleware' => ['auth.|basic',]]);""")
        selection = Selection(self.view)
        place = get_place(selection)
        self.assertEqual("Illuminate/Auth/Middleware/AuthenticateWithBasicAuth.php", place.path)


    def assertPath(self, expected, msg=None):
        selection = Selection(self.view)
        place = get_place(selection)

        self.assertIsNotNone(place, msg)
        self.assertEqual(expected, place.path, msg)

        return place;