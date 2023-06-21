import sublime
import sys
import os

from . import unittest
from LaravelGoto.lib.selection import Selection
from LaravelGoto.lib.place import get_place


class TestPlace(unittest.ViewTestCase):
    def test_controller_route(self):
        self.fixture("""
        Route::group(['namespace' => 'Resource'], function () {
            Route::controller('HelloController')->group(function () {
                Route::get('/posts/{id}', 'sh|ow');
            });
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual("Resource\\HelloController.php@show", place.path)

    def test_resource_route(self):
        self.fixture("""
        Route::group(['namespace' => 'Resource'], function () {
            Route::resource('photo', 'Hello|Controller', ['only' => [
                'index', 'show'
            ]]);
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual("Resource\\HelloController.php", place.path)

    def test_resource_route_action(self):
        self.fixture("""
        Route::group(['namespace' => 'Resource'], function () {
            Route::resource('photo', 'HelloController', ['only' => [
                'index', 'sho|w'
            ]]);
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual("Resource\\HelloController.php@show", place.path)

    def test_controller(self):
        self.fixture("""Route::get('/', 'HelloControll|er@index');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual("HelloController.php@index", place.path)

    def test_component(self):
        self.fixture("""<x-form.|input/>""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("form/input.php", place.path)

    def test_closing_tag_component(self):
        self.fixture("""</x-al|ert>""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("alert.php", place.path)

    def test_component_with_namespace(self):
        self.fixture("""<x-namespace::|alert/>""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("namespace/alert.php", place.path)

    def test_view(self):
        self.fixture("""
        Route::get('/', function () {
            return view('hello|_view');
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("hello_view.blade.php", place.path)

    def test_staticFile(self):
        self.fixture("""'hello|.JS';""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("hello.JS", place.path)

    def test_namespace58(self):
        self.fixture("""
        Route::namespace('58')->group(function () {
            Route::get('/', 'FiveEightC|ontroller@index');
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual('58\\FiveEightController.php@index', place.path)

    def test_namespace52(self):
        self.fixture("""
        Route::group(['namespace' => '52'], function () {
            Route::get('/', 'FiveTw|oController@index');
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual('52\\FiveTwoController.php@index', place.path)

    def test_namespaceLumen(self):
        self.fixture("""
        $router->group(['namespace' => 'Lumen'], function () use ($router) {
            Route::get('/', 'LumenCo|ntroller@index');
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual('Lumen\\LumenController.php@index', place.path)

    def test_view_namespace(self):
        self.fixture("""
        Route::get('/', function () {
            return view('Namespace::h|ello_view');
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('hello_view.blade.php', place.path)

    def test_absolute_path(self):
        self.fixture("""
        Route::group(['namespace' => 'Abc'], function () {
            Route::get('/', '\\Absolute\\IndexCont|roller@index')->name('index');
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual('\\Absolute\\IndexController.php@index', place.path)

    def test_facade_config_get(self):
        self.fixture("""Config::get('app.ti|mezone');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('config/app.php', place.path)
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_facade_config_set(self):
        self.fixture("""Config::set(   'app.timez|one', 'UTC');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('config/app.php', place.path)
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_config_get_only_file(self):
        self.fixture("""config('a|pp');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('config/app.php', place.path)

    def test_config_get_helper(self):
        self.fixture("""config('app.timez|one');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('config/app.php', place.path)
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_config_set_helper(self):
        self.fixture("""config(     ['app.timez|one' => 'UTC']);""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('config/app.php', place.path)
        self.assertEqual('([\'"]{1})timezone\\1\\s*=>', place.location)

    def test_env(self):
        self.fixture("""env(   'APP|_DEBUG', false);""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('.env', place.path)
        self.assertEqual('APP_DEBUG', place.location)

    def test_lang_underscore(self):
        self.fixture("""__('messages.w|elcome');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('lang/messages.php', place.path)

    def test_lang_blade_directive(self):
        self.fixture("""@lang('messages.we|lcome');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('lang/messages.php', place.path)

    def test_lang_trans(self):
        self.fixture("""trans('messages.we|lcome');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('lang/messages.php', place.path)

    def test_lang_trans_choice(self):
        self.fixture("""trans_choice('messages.a|pples', 10);""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('lang/messages.php', place.path)

    def test_lang_trans_package(self):
        self.fixture("""trans('package::messa|ges');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('lang/vendor/package/messages.php', place.path)

    def test_relative_path_static_file(self):
        self.fixture("""'./../../hel|lo.css'""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('hello.css', place.path)

    def test_package_view(self):
        self.fixture("""view('package::hell|o_view');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('package/hello_view.blade.php', place.path)

    def test_view_first(self):
        self.fixture("""View::first(['custom|.admin', 'admin'], $data);""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('custom/admin.blade.php', place.path)

    def test_view_exists(self):
        self.fixture("""View::exists('emails.c|ustomer');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('emails/customer.blade.php', place.path)

    def test_app_path(self):
        self.fixture("""app_path('Us|er.php');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('app/User.php', place.path)

    def test_config_path(self):
        self.fixture("""config_path('ap|p.php');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('config/app.php', place.path)

    def test_database_path(self):
        self.fixture("""database_path('UserFacto|ry.php');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('database/UserFactory.php', place.path)

    def test_public_path(self):
        self.fixture("""public_path('css/ap|p.css');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('public/css/app.css', place.path)

    def test_resource_path(self):
        self.fixture("""resource_path('sass/ap|p.scss');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('resources/sass/app.scss', place.path)

    def test_storage_path(self):
        self.fixture("""storage_path('logs/lara|vel.log');""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('storage/logs/laravel.log', place.path)

    def test_double_brackets_path(self):
        self.fixture("""realpath(storage_path('logs/lar|avel.log'));""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('storage/logs/laravel.log', place.path)

    def test_v8_namespace_route(self):
        self.fixture("""Route::get('/', [L8\\EightContro|ller::class, 'index']);""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual(True, place.is_controller)
        self.assertEqual('L8\\EightController.php@index', place.path)

    def test_v8_route(self):
        self.fixture("""Route::get('/', EightContro|ller::class);""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('EightController.php', place.path)

    def test_v8_group_namespae_abs_route(self):
        self.fixture("""
        Route::group(['namespace' => 'L8'], function () {
            Route::get('/', [\\EightControl|ler::class, 'index']);
        });""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual('\\EightController.php@index', place.path)

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

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("About/AboutComponent", place.path)

    def test_inertiajs_render(self):
        self.fixture("""Inertia::render("About/AboutC|omponent");""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("About/AboutComponent", place.path)

    def test_inertiajs_route(self):
        self.fixture("""Route::inertia("/about", "About/AboutCom|ponent");""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("About/AboutComponent", place.path)

    def test_livewire_tag(self):
        self.fixture("""<livewire:nav.sho|w-post />""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("Nav/ShowPost.php", place.path)

    def test_livewire_blade_directive(self):
        self.fixture("""@livewire("nav.show|-post")""")

        selection = Selection(self.view)
        place = get_place(selection)

        self.assertEqual("Nav/ShowPost.php", place.path)

