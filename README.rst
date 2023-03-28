=====
Django MySQL Binlog
=====

Django MySQL Binlog is a Django app to stream and act on change data from the MySQL binlog by dispatching and listening to Django signals.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "mysql_binlog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'mysql_binlog',
    ]
