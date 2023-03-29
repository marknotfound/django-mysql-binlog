from django.test import TestCase
from django.core.management import call_command
from mysql_binlog.exceptions import EmptyRegistryException
from mysql_binlog.registry import registry


class ConsumeBinLogCommandTest(TestCase):
    def test_handle_empty_registry(self):
        registry.reset()
        with self.assertRaises(EmptyRegistryException):
            call_command("consume_binlog")
