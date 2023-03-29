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

Running Tests
-----------
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install the requirements: `pip install -r requirements/test.txt`
4. Run the tests `python runtests.py`
