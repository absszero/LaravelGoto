from . import unittest
from unittest.mock import patch
from LaravelGoto.lib.language import Language


class TestLanguage(unittest.ViewTestCase):
    @patch('LaravelGoto.lib.workspace.get_folders')
    def test_get_place(self, mock_get_folders):
        mock_get_folders.return_value = [self.get_test_dir()]

        language = Language()
        place = language.get_place('blog.title')

        self.assertEqual(place.path, 'lang/blog.php')
        self.assertEqual(
            place.paths, [
                'lang/en/blog.php',
                'lang/fr/blog.php',
            ])
        self.assertEqual(len(place.uris), 2)

        # vendor
        place = language.get_place('pkg::blog.title')

        self.assertEqual(place.path, 'lang/vendor/pkg/blog.php')
        self.assertEqual(
            place.paths, [
                'lang/vendor/pkg/en/blog.php',
                'lang/vendor/pkg/fr/blog.php',
            ])
