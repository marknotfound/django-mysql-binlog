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

2. Register the models you wish to receive updates for. For example::

    # models.py

    from django.db import models
    from mysql_binlog.registry import registry

    @registry.register
    class Author(models.Model):
        name = models.CharField(max_length=255)

    @registry.register
    class Book(models.Model):
        author = models.ForeignKey(Author, on_delete=models.CASCADE)

3. Configure signal receivers for the signals you wish to listen to. For example::

    # signals.py
    from django.dispatch import receiver
    from mysql_binlog.signals import row_updated, row_created, row_deleted
    from models import Author, Book

    @receiver(row_created, sender=Author)
    def author_created(sender, instance, **kwargs):
        print("Author created!")

    @receiver(row_updated, sender=Book)
    def book_updated(sender, instance, before_values, after_values):
        print("Book updated!")

    @receiver(row_deleted, sender=Book)
    def book_deleted(sender, instance, **kwargs):
        # Be careful what you do with `instance` here.
        # It is a model instance with data hydrated from the binlog event
        # so most normal properties should be available.
        print("Book deleted!")


4. Run the binlog consumer command::

    python manage.py consume_binlog


Running Tests
-----------
1. Create a virtual environment: `python -m venv venv`
2. Activate the virtual environment: `source venv/bin/activate`
3. Install the requirements: `pip install -r requirements/test.txt`
4. Run the tests `python runtests.py`
