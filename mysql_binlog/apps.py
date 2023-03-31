from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class MysqlBinlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mysql_binlog"

    def ready(self) -> None:
        autodiscover_modules("models")
