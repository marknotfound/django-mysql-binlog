from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.cache import cache
from django.db.models import Model
from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.row_event import (
    DeleteRowsEvent,
    UpdateRowsEvent,
    WriteRowsEvent,
)

from mysql_binlog.registry import registry
from mysql_binlog.signals import row_created, row_updated, row_deleted
from mysql_binlog.exceptions import EmptyRegistryException


CACHE_KEY_LOG_POS = "django_mysql_binlog_log_pos"
CACHE_KEY_LOG_FILE = "django_mysql_binlog_log_file"


def get_pk(binlog_event, row) -> int:
    if isinstance(binlog_event, UpdateRowsEvent):
        return row["after_values"]["id"]
    return row["values"]["id"]


def get_instance(binlog_event, row) -> Model:
    ModelClass = registry.get_model_for_table(binlog_event.table)
    pk = get_pk(binlog_event, row)

    if isinstance(binlog_event, DeleteRowsEvent):
        return ModelClass(pk=pk, **row["values"])
    return ModelClass.objects.get(pk=pk)


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not registry.tables:
            raise EmptyRegistryException("No models registered for binlog consumption")

        database = settings.DATABASES["default"]
        stream = BinLogStreamReader(
            connection_settings={
                "host": database["HOST"],
                "port": int(database["PORT"]),
                "user": database["USER"],
                "passwd": database["PASSWORD"],
            },
            server_id=1,
            blocking=True,
            resume_stream=True,
            only_events=[DeleteRowsEvent, WriteRowsEvent, UpdateRowsEvent],
            log_pos=cache.get(CACHE_KEY_LOG_POS, None),
            log_file=cache.get(CACHE_KEY_LOG_FILE, None),
            only_tables=registry.tables,
        )

        for binlog_event in stream:
            for row in binlog_event.rows:
                instance = get_instance(binlog_event, row)
                if isinstance(binlog_event, DeleteRowsEvent):
                    row_deleted.send_robust(
                        sender=instance.__class__, instance=instance
                    )
                elif isinstance(binlog_event, WriteRowsEvent):
                    row_created.send_robust(
                        sender=instance.__class__, instance=instance
                    )
                elif isinstance(binlog_event, UpdateRowsEvent):
                    row_updated.send_robust(
                        sender=instance.__class__,
                        instance=instance,
                        before_values=row["before_values"],
                        after_values=row["after_values"],
                    )

            cache.set(CACHE_KEY_LOG_POS, stream.log_pos)
            cache.set(CACHE_KEY_LOG_FILE, stream.log_file)

        stream.close()
