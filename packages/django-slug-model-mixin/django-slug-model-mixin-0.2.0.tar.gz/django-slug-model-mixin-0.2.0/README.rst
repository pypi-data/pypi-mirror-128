=============================
Django Slug Model Mixin
=============================

.. image:: https://badge.fury.io/py/django-slug-model-mixin.svg
    :target: https://badge.fury.io/py/django-slug-model-mixin

.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
    :target: https://django-slug-model-mixin.readthedocs.io/en/latest/

.. image:: https://img.shields.io/coveralls/github/frankhood/django-slug-model-mixin/main?style=flat-square
    :target: https://coveralls.io/github/frankhood/django-slug-model-mixin?branch=main
    :alt: Coverage Status

Slugify model mixin to manage slugged fields in your project models.

Documentation
-------------

The full documentation is at https://django-slug-model-mixin.readthedocs.io.

Quickstart
----------

Install Django Slug Model Mixin::

    pip install django-slug-model-mixin

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'slug_model_mixin',
        ...
    )

Use the SlugModelMixin in your model:

.. code-block:: python

    class ExampleModel(SlugModelMixin, models.Model):
        slugged_field = 'name'  # insert the name of the field you want to slugify
        slug_unique = False # remove unique for your slug
        force_slugify = True # force the slugify using uuslug

        name = models.CharField(
            'Name',
            max_length=255
        )

    class Meta:
        verbose_name = 'Example Model'
        verbose_name_plural = 'Example Models'


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
