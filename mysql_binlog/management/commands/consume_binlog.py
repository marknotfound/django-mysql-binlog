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

from registry import registry
from signals import row_created, row_updated, row_deleted


CACHE_KEY_LOG_POS = "django_mysql_binlog_log_pos"
CACHE_KEY_LOG_FILE = "django_mysql_binlog_log_file"


def get_pk(binlogevent, row) -> int:
    if isinstance(binlogevent, UpdateRowsEvent):
        return row["after_values"]["id"]
    return row["values"]["id"]


def get_instance(binlogevent, row) -> Model:
    ModelClass = registry.get_model_for_table(binlogevent.table)
    pk = get_pk(binlogevent, row)

    if isinstance(binlogevent, DeleteRowsEvent):
        return ModelClass(pk=pk, **row["values"])
    return ModelClass.objects.get(pk=pk)


class Command(BaseCommand):
    def handle(self, *args, **options):
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

        for binlogevent in stream:
            for row in binlogevent.rows:
                instance = get_instance(binlogevent, row)
                if isinstance(binlogevent, DeleteRowsEvent):
                    row_deleted.send_robust(
                        sender=instance.__class__, instance=instance
                    )
                elif isinstance(binlogevent, WriteRowsEvent):
                    row_created.send_robust(
                        sender=instance.__class__, instance=instance
                    )
                elif isinstance(binlogevent, UpdateRowsEvent):
                    row_updated.send_robust(
                        sender=instance.__class__,
                        instance=instance,
                        before_values=row["before_values"],
                        after_values=row["after_values"],
                    )

            cache.set(CACHE_KEY_LOG_POS, stream.log_pos)
            cache.set(CACHE_KEY_LOG_FILE, stream.log_file)

        stream.close()
