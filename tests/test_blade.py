from . import unittest
from LaravelGoto.lib.blade import Blade


class TestBlade(unittest.ViewTestCase):
    blade = Blade()

    def test_view(self):
        place = self.blade.get_place(
            'hello_view',
            "return view('hello_view');"
        )
        self.assertEqual("hello_view.blade.php", place.path)

        # namespace
        place = self.blade.get_place(
            'Namespace::hello_view',
            "return view('Namespace::hello_view');"
        )
        self.assertEqual('hello_view.blade.php', place.path)

        # package
        place = self.blade.get_place(
            'package::hello_view',
            "view('package::hello_view');"
        )
        self.assertEqual('package/hello_view.blade.php', place.path)

        # notification markdown view
        place = self.blade.get_place(
            'hello_view',
            "markdown('hello_view');"
        )
        self.assertEqual('hello_view.blade.php', place.path)

    def test_view_var(self):
        place = self.blade.get_place('hello_view', "$view = 'hello_view'")
        self.assertEqual("hello_view.blade.php", place.path)

    def test_view_in_mailable(self):
        place = self.blade.get_place('emails.test', "view: 'emails.test',")
        self.assertEqual("emails/test.blade.php", place.path)

        place = self.blade.get_place('emails.test', "text: 'emails.test',")
        self.assertEqual("emails/test.blade.php", place.path)

        place = self.blade.get_place('emails.test', "html: 'emails.test',")
        self.assertEqual("emails/test.blade.php", place.path)

        place = self.blade.get_place('emails.test', "markdown: 'emails.test',")
        self.assertEqual("emails/test.blade.php", place.path)

    def test_view_in_route_view(self):
        place = self.blade.get_place(
            'pages.welcome',
            "Route::view('/', 'pages.welcome');"
        )
        self.assertEqual("pages/welcome.blade.php", place.path)

    def test_layout_method(self):
        place = self.blade.get_place('hello_view', "layout('hello_view');")
        self.assertEqual("hello_view.blade.php", place.path)

    def test_view_in_config_livewire_php(self):
        place = self.blade.get_place(
            'layouts.app',
            "'layout' => 'layouts.app',"
        )
        self.assertEqual("layouts/app.blade.php", place.path)

    def test_blade_include_and_includeIf(self):
        place = self.blade.get_place(
            'view.name',
            "@includeIf('view.name', ['status' => 'complete'])"
        )
        self.assertEqual("view/name.blade.php", place.path)

        place = self.blade.get_place(
            'view.name',
            "@include('view.name', ['status' => 'complete'])"
            )
        self.assertEqual("view/name.blade.php", place.path)

    def test_blade_extends(self):
        place = self.blade.get_place('view.name', "@extends('view.name')")
        self.assertEqual("view/name.blade.php", place.path)

    def test_blade_inclcudeUnless_and_inclcudeWhen(self):
        place = self.blade.get_place(
            'view.name',
            "@includeUnless($boolean, 'view.name')"
        )
        self.assertEqual("view/name.blade.php", place.path)

        place = self.blade.get_place(
            'view.name',
            "@includeWhen($boolean, 'view.name')"
        )
        self.assertEqual("view/name.blade.php", place.path)

    def test_view_exists(self):
        place = self.blade.get_place(
            'emails.customer',
            "View::exists('emails.customer');"
        )
        self.assertEqual('emails/customer.blade.php', place.path)

    def test_view_composer(self):
        place = self.blade.get_place(
            'profile',
            "View::composer('profile', ProfileComposer::class);"
        )
        self.assertEqual('profile.blade.php', place.path)

    def test_view_creator(self):
        place = self.blade.get_place(
            'profile',
            "View::creator('profile', ProfileComposer::class);"
        )
        self.assertEqual('profile.blade.php', place.path)

    def test_view_resource_string(self):
        place = self.blade.get_place(
            'resources/views/pages/public/charge',
            "'resources/views/pages/public/charge'"
        )
        self.assertEqual(
            'resources/views/pages/public/charge.blade.php',
            place.path
        )

        place = self.blade.get_place(
            'resources/views/components/layout',
            "'{{-- resources/views/components/layout --}}'"
        )
        self.assertEqual(
            'resources/views/components/layout.blade.php',
            place.path
        )

        place = self.blade.get_place(
            'resources/views/components/layout.blade.php',
            "'resources/views/components/layout.blade.php'"
        )
        self.assertEqual(
            'resources/views/components/layout.blade.php',
            place.path
        )

    def test_blade_includeFirst(self):
        place = self.blade.get_place(
            'custom.admin',
            "@includeFirst(['custom.admin', 'admin'])"
        )
        self.assertEqual("custom/admin.blade.php", place.path)

        place = self.blade.get_place(
            'admin',
            "@includeFirst(['custom.admin', 'admin'])"
        )
        self.assertEqual("admin.blade.php", place.path)

    def test_notification_multi_view(self):
        place = self.blade.get_place(
            'emails.name.html',
            "view(['emails.name.html', 'emails.name.plain']);"
        )
        self.assertEqual("emails/name/html.blade.php", place.path)

        place = self.blade.get_place(
            'emails.name.plain',
            "view(['emails.name.html', 'emails.name.plain']);"
        )
        self.assertEqual("emails/name/plain.blade.php", place.path)

    def test_view_multi_composer(self):
        place = self.blade.get_place(
            'profile',
            "View::composer(['profile', 'dashboard'], A::class);"
        )
        self.assertEqual('profile.blade.php', place.path)

        place = self.blade.get_place(
            'dashboard',
            "View::composer(['profile', 'dashboard'], A::class);"
        )
        self.assertEqual('dashboard.blade.php', place.path)

        place = self.blade.get_place(
            'profile',
            "View::composer('profile', ProfileComposer::class);"
        )
        self.assertEqual('profile.blade.php', place.path)

    def test_blade_each(self):
        place = self.blade.get_place(
            'view.name',
            "@each('view.name', $jobs, 'job', 'view.empty')"
            )
        self.assertEqual("view/name.blade.php", place.path)

        place = self.blade.get_place(
            'view.empty',
            "@each('view.name', $jobs, 'job', 'view.empty')"
            )
        self.assertEqual("view/empty.blade.php", place.path)

    def test_view_first(self):
        place = self.blade.get_place(
            'custom.admin',
            "View::first(['custom.admin', 'admin'], $data);"
            )
        self.assertEqual('custom/admin.blade.php', place.path)
        place = self.blade.get_place(
            'admin',
            "View::first(['custom.admin', 'admin'], $data);"
            )
        self.assertEqual('admin.blade.php', place.path)

    def test_multiline(self):
        place = self.blade.get_place(
            'hello_view',
            "'hello_view', ['name' => 'James']",
            """view(
                'hello_view', ['name' => 'James']
            );"""
        )
        self.assertEqual('hello_view.blade.php', place.path)
