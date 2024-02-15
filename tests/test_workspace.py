import os

from . import unittest
from LaravelGoto.lib import workspace


class TestWorkspace(unittest.ViewTestCase):
    def test_get_file_content(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        content = workspace.get_file_content(folder, 'app/Http/Kernel.php')
        self.assertTrue(
            content.__contains__('class Kernel extends HttpKernel')
            )

    def test_get_path(self):
        folder = os.path.dirname(os.path.abspath(__file__))
        fullpath = workspace.get_path(folder, 'app/Http/Kernel.php')
        self.assertTrue(fullpath.__contains__('app/Http/Kernel.php'))

        fullpath = workspace.get_path(folder, 'unittest.py')
        self.assertTrue(fullpath.__contains__('unittest.py'))

        fullpath = workspace.get_path(folder, 'sample.php')
        self.assertTrue(fullpath.__contains__('sample.php'))

    def test_get_recursion_files(self):
        folder = os.path.dirname(os.path.abspath(__file__)) +\
            '/fixtures/app/Console/Commands'
        files = workspace.get_recursion_files(folder)
        files.sort()
        self.assertTrue(files[0].endswith('SayGoodbye.php'), files[0])
        self.assertTrue(files[1].endswith('SayHello.php'), files[1])
        self.assertTrue(files[2].endswith('SendEmails.php'), files[2])

    def test_class_2_file(self):
        filename = workspace.class_2_file("\\App\\NS\\SayGoodbye::class,")
        self.assertEqual(filename, 'app/NS/SayGoodbye.php')

    def test_get_folder_path(self):
        base = os.path.dirname(os.path.abspath(__file__))

        path = workspace.get_folder_path(base, 'fixtures')
        self.assertTrue(path.endswith('fixtures'), path)

        folders = workspace.get_folder_path(base, 'resources/lang/*')
        self.assertEqual(len(folders), 2)

        path = workspace.get_folder_path(base, 'fixtures/config')
        self.assertTrue(path.endswith('config'), path)

        path = workspace.get_folder_path(base, 'config')
        self.assertTrue(path.endswith('config'), path)

        path = workspace.get_folder_path(base, 'app/Http')
        self.assertTrue(path.endswith('Http'), path)

        # # over 2 layer directories
        path = workspace.get_folder_path(base, 'Http')
        self.assertFalse(path)

    def test_changed(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.assertTrue(workspace.is_changed(base))
        self.assertTrue(workspace.is_changed(base, __file__))
        self.assertFalse(workspace.is_changed(base, '/aaa/bbb'))
        workspace.set_unchanged(base)
        self.assertFalse(workspace.is_changed(base), 'post')
        self.assertFalse(workspace.is_changed(base, __file__))
