from typing import Type, TypeVar
from django.db.models import Model

_M = Type[Model]
_TM = TypeVar("_TM", bound=_M)


class Registry:
    models: set[_M] = set()
    tables: set[str] = set()
    table_models: dict[str, _M] = dict()

    def register(self, model: _TM) -> _TM:
        table = model._meta.db_table
        self.models.add(model)
        self.tables.add(table)
        self.table_models[table] = model
        return model

    def is_model_registered(self, model: _M) -> bool:
        return model in self.models

    def get_model_for_table(self, table: str) -> _M:
        return self.table_models[table]


registry = Registry()

__all__ = [
    "registry",
    "Registry",
]
