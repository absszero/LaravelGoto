from . import unittest
from LaravelGoto.lib.helper import Helper


class TestHelper(unittest.ViewTestCase):
    helper = Helper()

    def test_app_path(self):
        place = self.helper.get_place('User.php', """app_path('User.php');""")
        self.assertEqual('app/User.php', place.path)

    def test_config_path(self):
        place = self.helper.get_place('app.php', """config_path('app.php');""")
        self.assertEqual('config/app.php', place.path)

    def test_database_path(self):
        place = self.helper.get_place('UserFactory.php', """database_path('UserFactory.php');""")
        self.assertEqual('database/UserFactory.php', place.path)

    def test_public_path(self):
        place = self.helper.get_place('css/app.css', """public_path('css/app.css');""")
        self.assertEqual('public/css/app.css', place.path)

    def test_resource_path(self):
        place = self.helper.get_place('sass/app.scss', """resource_path('sass/app.scss');""")
        self.assertEqual('resources/sass/app.scss', place.path)

    def test_storage_path(self):
        place = self.helper.get_place('logs/laravel.log', """storage_path('logs/laravel.log');""")
        self.assertEqual('storage/logs/laravel.log', place.path)

    def test_double_brackets_path(self):
        place = self.helper.get_place('logs/laravel.log', """realpath(storage_path('logs/laravel.log'));""")
        self.assertEqual('storage/logs/laravel.log', place.path)

    def test_to_action(self):
        place = self.helper.get_place('show', """to_action([UserController::class, 'show'], ['user' => 1]);""")
        self.assertEqual('UserController.php@show', place.path)
