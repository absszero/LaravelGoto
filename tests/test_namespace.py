from . import unittest
from LaravelGoto.lib.selection import Selection
from LaravelGoto.lib.namespace import Namespace


class TestNamespace(unittest.ViewTestCase):
    def test_sibling_namespace(self):
        self.fixture("""
        Route::namespace('58')->group(function () {
            Route::get('/', 'HelloController@index');
        });

        Route::group(['namespace' => '52'], function () {
            Route::get('/', 'HelloContro|ller@index');
        });""")

        selection = Selection(self.view)
        namespace = Namespace(self.view)
        blocks = namespace.get_blocks(selection)

        self.assertEqual(1, len(blocks))
        self.assertEqual("52", blocks[0]['namespace'])

    def test_group_namespace(self):
        self.fixture("""
        Route::group(['namespace' => '52'], function () {
            Route::get('/', 'HelloController@i|ndex');
        });""")

        selection = Selection(self.view)
        namespace = Namespace(self.view)
        blocks = namespace.get_blocks(selection)

        self.assertEqual("52", blocks[0]['namespace'])

    def test_route_namespace(self):
        self.fixture("""
        Route::namespace('58')->group(function () {
            Route::get('/', 'HelloControll|er@index');
        });""")

        selection = Selection(self.view)
        namespace = Namespace(self.view)
        blocks = namespace.get_blocks(selection)

        self.assertEqual("58", blocks[0]['namespace'])

    def test_class_controller(self):
        self.fixture("""
        Route::controller(HelloController::class)->group(function () {
            Route::get('/post|s/{id}', 'show');
            Route::post('/posts', 'store');
        });""")

        selection = Selection(self.view)
        namespace = Namespace(self.view)
        blocks = namespace.get_blocks(selection)

        self.assertEqual("HelloController", blocks[0]['namespace'])
        self.assertFalse(blocks[0]['is_namespace'])

    def test_string_controller(self):
        self.fixture("""
        Route::controller('HelloController')->group(function () {
            Route::get('/post|s/{id}', 'show');
            Route::post('/posts', 'store');
        });""")

        selection = Selection(self.view)
        namespace = Namespace(self.view)
        blocks = namespace.get_blocks(selection)

        self.assertEqual("HelloController", blocks[0]['namespace'])
        self.assertFalse(blocks[0]['is_namespace'])

    def test_resource(self):
        self.fixture("""
        Route::group(['namespace' => 'Resource'], function () {
            Route::resource('photo', 'HelloController', ['only' => [
                'ind|ex', 'show'
            ]]);
        });""")

        selection = Selection(self.view)
        namespace = Namespace(self.view)
        blocks = namespace.get_blocks(selection)

        self.assertEqual("Resource", blocks[1]['namespace'])
