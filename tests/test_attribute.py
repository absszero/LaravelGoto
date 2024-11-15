from . import unittest
from LaravelGoto.lib.attribute import Attribute


class TestBlade(unittest.ViewTestCase):
    attribute = Attribute()

    def test_contextual_attributes(self):
        place = self.attribute.get_place('web', "#[Auth('web')]")
        self.assertEqual("config/auth.php", place.path)
        self.assertEqual("""['"]web['"]\\s*=>""", place.location)

        place = self.attribute.get_place('redis', "#[Cache('redis')]")
        self.assertEqual("config/cache.php", place.path)
        self.assertEqual("""['"]redis['"]\\s*=>""", place.location)

        place = self.attribute.get_place('app.timezone', "#[Config('app.timezone')]")
        self.assertEqual("config/app.php", place.path)
        self.assertEqual("""['"]timezone['"]\\s*=>""", place.location)

        place = self.attribute.get_place('mysql', "#[DB('mysql')]")
        self.assertEqual("config/database.php", place.path)
        self.assertEqual("""['"]mysql['"]\\s*=>""", place.location)

        place = self.attribute.get_place('daily', "#[Log('daily')]")
        self.assertEqual("config/logging.php", place.path)
        self.assertEqual("""['"]daily['"]\\s*=>""", place.location)

        place = self.attribute.get_place('s3', "#[Storage('s3')]")
        self.assertEqual("config/filesystems.php", place.path)
        self.assertEqual("""['"]s3['"]\\s*=>""", place.location)
