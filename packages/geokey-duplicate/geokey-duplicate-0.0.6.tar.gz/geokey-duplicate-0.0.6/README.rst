.. image:: https://img.shields.io/pypi/v/geokey-duplicate.svg
    :alt: PyPI Package
    :target: https://pypi.python.org/pypi/geokey-duplicate

.. image:: https://www.travis-ci.com/ExCiteS/geokey-duplicate.svg?branch=main
    :alt: Travis CI Build Status
    :target: https://www.travis-ci.com/github/ExCiteS/geokey-duplicate/

.. image:: https://img.shields.io/coveralls/ExCiteS/geokey-duplicate/master.svg
    :alt: Coveralls Test Coverage
    :target: https://coveralls.io/r/ExCiteS/geokey-duplicate


geokey-duplicate
================

Duplicate project and categories

Download all observations
Currently supported formats:

- KML
- GeoJSON
- XLXS 

Install
-------

geokey-duplicate requires:

- Python version 2.7
- GeoKey version 1.6 or greater

Install the extension from PyPI:

.. code-block:: console

    pip install geokey-duplicate

Or from cloned repository:

.. code-block:: console

    cd geokey-duplicate
    pip install -e .

Add the package to installed apps:

.. code-block:: python

    INSTALLED_APPS += (
        ...
        'geokey_duplicate',
    )

Migrate the models into the database:

.. code-block:: console

    python manage.py migrate geokey_duplicate

Copy static files:

.. code-block:: console

    python manage.py collectstatic

You're now ready to go!

Test
----

Run tests:

.. code-block:: console

    python manage.py test geokey_duplicate

Check code coverage:

.. code-block:: console

    coverage run --source=geokey_duplicate manage.py test geokey_duplicate
    coverage report -m --omit=*/tests/*,*/migrations/*
