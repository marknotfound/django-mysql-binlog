from django.test import TestCase
from django.db import models
from mysql_binlog.registry import Registry

registry = Registry()


@registry.register
class Book(models.Model):
    page_count = models.IntegerField()


class RegistryTest(TestCase):
    def test_is_model_registered(self):
        self.assertTrue(
            registry.is_model_registered(Book),
        )

    def test_get_models_for_table(self):
        self.assertEqual(
            registry.get_model_for_table(Book._meta.db_table),
            Book,
        )
