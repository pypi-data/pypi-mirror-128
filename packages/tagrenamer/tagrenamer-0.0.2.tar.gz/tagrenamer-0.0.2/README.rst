==========
tagrenamer
==========

.. image:: https://img.shields.io/github/languages/top/nielsvm/tagrenamer.svg
        :target: https://github.com/nielsvm/tagrenamer

.. image:: https://img.shields.io/github/license/nielsvm/tagrenamer.svg
        :target: https://raw.githubusercontent.com/nielsvm/tagrenamer/master/LICENSE

.. image:: https://img.shields.io/pypi/v/tagrenamer.svg
        :target: https://pypi.python.org/pypi/tagrenamer

.. image:: https://img.shields.io/readthedocs/tagrenamer.svg
        :target: https://tagrenamer.readthedocs.io/

*Mass music collection renamer.*

**Tagrenamer completely cleans up your music folder for you, all you need**
**to do is to make sure all music files have the right tags.**

Imagine this is inside your music folder:

.. code-block:: console

   Music/
   ├── MUTTER (2001) - Adios.mp3
   ├── MUTTER (2001) - Feuer Frei.mp3
   ├── MUTTER (2001) - Ich Will.mp3
   ├── MUTTER (2001) - Links 2 3 4.mp3
   ├── MUTTER (2001) - Mein Herz Brennt.mp3
   ├── MUTTER (2001) - Mutter.mp3
   ├── MUTTER (2001) - Nebel.mp3
   ├── MUTTER (2001) - Rein Raus.mp3
   ├── MUTTER (2001) - Sonne.mp3
   ├── MUTTER (2001) - Spieluhr.mp3
   └── MUTTER (2001) - Zwitter.mp3

What a mess, let's clean it up:

.. code-block:: console

   $ tagrenamer --format '{artist}/{album}/{artist}-{title}.{ext}' Music/
    - Tagrenamer version 0.0.2.
    - Leftovers directory '__LEFTOVERS/' created.
    - Stage directory '__STAGE/' created.
    - Traverse the collection and extract music tags.
    - Validating tag input and sanitizing variables.
    - Moving non music files to '__LEFTOVERS/'.
    - Moving music to new tree in stage directory '__STAGE/'.
    - Remove empty directories (except stage/leftover directories).
    - Move everything from stage into the final location.
    - Deleting the temporary stage directory '__STAGE/'.
    - Deleting the empty leftovers directory '__LEFTOVERS/'.
    - DONE! Processed 11 files.

.. code-block:: console

   Music/
   └── rammstein
       └── mutter
           ├── rammstein-adios.mp3
           ├── rammstein-feuer frei.mp3
           ├── rammstein-ich will.mp3
           ├── rammstein-links 2 3 4.mp3
           ├── rammstein-mein herz brennt.mp3
           ├── rammstein-mutter.mp3
           ├── rammstein-nebel.mp3
           ├── rammstein-rein raus.mp3
           ├── rammstein-sonne.mp3
           ├── rammstein-spieluhr.mp3
           └── rammstein-zwitter.mp3

Features
--------

#. **Python**

   Pure Python command-line application that is cross-platform and strives to
   meet all modern quality criteria such as PEP8-compliance and test coverage.
#. **Formats**

   Supports ``.mp3``, ``.ogg`` and ``.flac`` files and more are easy to add.

#. **Only deals with music**

   Files that are not music, are moved into a folder named ``__LEFTOVERS/``
   which contains the original structure they were originally in. Letting you
   decide what to do with them.

#. **Fail-safe**

   Tagrenamer leverages an internal staging process in which it detects failures
   before it touched a single file. The paranoid can combine ``--dry-run`` and
   ``-vvvv`` to see what is going on under the hood or even run with ``--shell``
   to generate Shell commands for you to inspect without renaming anything.

#. **Scalability**

   Renames a few music albums as well as a 2Tb music collection.

Installation
------------

Install Tagrenamer directly from `PyPI`_ using ``pip``:

.. code-block:: console

   $ pip3 install tagrenamer

.. _PyPI: https://pypi.org/project/tagrenamer/
