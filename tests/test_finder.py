from unittest.mock import patch
from . import unittest

from LaravelGoto.lib.selection import Selection
from LaravelGoto.lib.finder import get_place
from LaravelGoto.lib.place import Place


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
        self.assertPath("views/components/form/input.blade.php")

    def test_closing_tag_component(self):
        self.fixture("""</x-hello-al|ert>""")
        place = self.assertPath("views/components/hello-alert.blade.php")
        self.assertEqual(
            place.paths[0],
            'views/components/hello-alert.blade.php'
            )
        self.assertEqual(place.paths[1], 'View/Components/HelloAlert.php')

    def test_contextual_attributes(self):
        self.fixture("""#[Config('app.time|zone')]""")
        self.assertPath("config/app.php")

    def test_component_with_namespace(self):
        self.fixture("""<x-namespace::|alert/>""")
        self.assertPath("namespace/alert.blade.php")

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

    def test_absolute_path(self):
        self.fixture("""
        Route::group(['namespace' => 'Abc'], function () {
            Route::get('/', '\\Absolute\\IndexCont|roller@index');
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

    def test_filesystem_config(self):
        self.fixture("""Storage::disk('loc|al')->put('a.txt', 'b');""")
        place = self.assertPath('config/filesystems.php')
        self.assertEqual('([\'"]{1})local\\1\\s*=>', place.location)

    def test_env(self):
        self.fixture("""env(   'APP|_DEBUG', false);""")
        place = self.assertPath('.env')
        self.assertEqual('APP_DEBUG', place.location)

    def test_lang_underscore(self):
        self.fixture("""__('messages.w|elcome');""")
        self.assertPath('lang/messages.php')

        self.fixture("""@lang('messages.we|lcome');""")
        self.assertPath('lang/messages.php')

        self.fixture("""trans('messages.we|lcome');""")
        self.assertPath('lang/messages.php')

        self.fixture("""trans_choice('messages.a|pples', 10);""")
        self.assertPath('lang/messages.php')

    def test_relative_path_static_file(self):
        self.fixture("""'./../../hel|lo.css'""")
        self.assertPath('hello.css')

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
        self.fixture(
            """Route::get('/', [L8\\EightController::class, 'in|dex']);"""
            )

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
            Route::get('/', [\\EightController::class, 'ind|ex']);
        });""")
        self.assertPath('\\EightController.php@index')

    def test_v8_group_namespae_route(self):
        self.fixture("""
        Route::group(['namespace' => 'L8'], function () {
            Route::get('/', [EightController::class, 'ind|ex']);
        });""")

        selection = Selection(self.view)
        place = get_place(selection)
        self.assertEqual(True, place.is_controller)
        self.assertEqual('L8\\EightController.php@index', place.path)

    def test_inertiajs_function(self):
        self.fixture("""inertia("About/AboutCo|mponent");""")
        self.assertPath("About/AboutComponent")

    def test_livewire_tag(self):
        self.fixture("""<livewire:nav.sho|w-post />""")
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

    @patch('LaravelGoto.lib.finder.Middleware.all')
    def test_middleware(self, mock_middleware):
        mock_middleware.return_value = {
            'auth': Place('App/Http/Middleware/Authenticate.php'),
            'auth.basic': Place('Illuminate/Auth/Middleware/BasicAuth.php')
        }
        self.fixture("""Route::middleware(['web:1234', 'auth|:abc']);""")
        self.assertPath("App/Http/Middleware/Authenticate.php")

        self.fixture("""Route::group(['middleware' => ['auth.|basic',]]);""")
        self.assertPath("Illuminate/Auth/Middleware/BasicAuth.php")

    @patch('LaravelGoto.lib.finder.Console.all')
    def test_command(self, mock_console):
        mock_console.return_value = {
            'app:say-hello': Place('SayHello.php'),
        }
        self.fixture("""Artisan::call('app:say|-hello --args');""")
        self.assertPath("SayHello.php")

        self.fixture("""command('app:say|-hello --args');""")
        self.assertPath("SayHello.php")

    def assertPath(self, expected, msg=None):
        selection = Selection(self.view)
        place = get_place(selection)

        self.assertIsNotNone(place, msg)
        self.assertEqual(expected, place.path, msg)

        return place
