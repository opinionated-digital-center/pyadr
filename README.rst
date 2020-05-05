================
ADR Process Tool
================

.. image:: https://github.com/opinionated-digital-center/pyadr/workflows/Test%20and%20make%20release/badge.svg
    :target: https://github.com/opinionated-digital-center/pyadr/actions

.. image:: https://github.com/opinionated-digital-center/pyadr/workflows/Publish%20Python%20package%20to%20Pypi/badge.svg
    :target: https://github.com/opinionated-digital-center/pyadr/actions

.. image:: https://img.shields.io/pypi/v/pyadr.svg
    :target: https://pypi.org/project/pyadr/

.. image:: https://img.shields.io/pypi/status/pyadr.svg
    :target: https://pypi.org/project/pyadr/

.. image:: https://img.shields.io/pypi/pyversions/pyadr.svg
    :target: https://pypi.org/project/pyadr/

.. image:: https://img.shields.io/pypi/l/pyadr.svg
    :target: https://pypi.org/project/pyadr/


CLI to help with an ADR process lifecycle (``proposal``/``approval``/``rejection``/``deprecation``/
``superseding``) based on ``markdown`` files and ``git``.

*This tools is in pre-alpha state. Sphinx doc to be updated.*

Features
--------

``pyadr``
+++++++++

* ``pyadr init``: initialise an ADR repository.
* ``pyadr new|propose Title of your ADR``: propose a new ADR.
* ``pyadr accept [<file-path>]``: accept a proposed ADR.
* ``pyadr reject [<file-path>]``: reject a proposed ADR.
* ``pyadr deprecate <file-path>``: (not yet implemented) deprecate an ADR.
* ``pyadr supersede <superseded-file-path> <superseding-file-path>``: (not yet implemented) supersede an ADR with another ADR.
* ``pyadr generate-toc``: generate a table of content (in format ``index.md``).
* ``pyadr config [<setting>] [<value>]``: configure a setting.

Help for all commands is available through ``pyadr help``.

Help for individual commands is available through ``pyadr help <command>``.

``git adr``
+++++++++++

The ``git`` extension to ``pyadr`` does the following additional actions:

* ``git adr init``:

  * initialise a git repository for the ADRs.

* ``git adr new|propose Title of your ADR``:

  * create a new branch from ``master``.
  * stage the new ADR in that branch.

* ``git adr accept [<file-path>]``:

  * stage ADR to current branch.
  * optionally commit ADR.
  * optionally squash commits.

* ``git adr reject [<file-path>]``:

  * stage ADR to current branch.
  * optionally commit ADR.
  * optionally squash commits.

* ``git adr deprecate <file-path>``: (not yet implemented)

  * create a new branch from ``master``.
  * stage the deprecated ADR in that branch.
  * optionally commit.
  * optionally squash commits.

* ``git adr supersede <superseded-file-path> <superseding-file-path>``: (not yet implemented)

  * create a new branch from ``master``.
  * stage the superseded and superseding ADRs in that branch.
  * optionally commit both ADRs.
  * optionally squash commits.

* ``git adr commit <proposal|acceptance|rejection|deprecation|superseding> <file-path> [<superseding-file-path>]``: (not yet implemented)

  * optionally stage ADR(s) to current branch.
  * commit ADR(s).
  * optionally squash commits.

* ``pyadr config [<setting>] [<value>]``:

  * configure also settings specific to ``git adr``.

Help for all commands is available through ``git adr help``.

Help for individual commands is available through ``git adr help <command>``.

Process Details
---------------

(Needs rewriting)

Once a proposed ADR placed in the ``docs/adr`` directory has been reviewed by peers, you can either action the decision
to accept it (``pyadr accept``) or to reject it (``pyadr reject``), which will:

* Update the ADR content by:

  * Changing the ADR status (``accepted`` or ``rejected``)
  * Changing the ADR date to current date

* Change the ADR file name from ``XXXX-<whatever-is-here>`` to
  ``<next-available-id>-<adr-title-in-lowercase>`` (follows
  `MADR-0005-format <https://github.com/adr/madr/blob/2.1.2/docs/adr/0005-use-dashes-in-filenames.md>`_)

Various safety checks are performed before these actions take place. See BDD tests
in the ``features`` directory.

Installation
------------

To install ADR Process Tool, run:

.. code-block:: console

    $ pip install pyadr

Credits
-------

This package was created with Cookiecutter_ and the
`opinionated-digital-center/python-library-project-generator`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`opinionated-digital-center/python-library-project-generator`: https://github.com/opinionated-digital-center/python-library-project-generator
