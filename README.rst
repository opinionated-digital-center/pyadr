================
ADR Process Tool
================

.. image:: https://img.shields.io/pypi/v/pyadr.svg
        :target: https://pypi.python.org/pypi/pyadr

.. image:: https://gitlab.com/opinionated-digital-center/pyadr/badges/master/pipeline.svg
    :target: https://gitlab.com/opinionated-digital-center/pyadr/pipelines
    :alt: Linux build

CLI to help with an ADR process lifecycle (proposal/approval/rejection/deprecation/
superseeding) based on Markdown files and git.

* Free software license: MIT

**This tools is in pre-alpha state. Sphinx do to be updated.**

Features
--------

* Accept or reject a proposed ADR.

Process Details
+++++++++++++++

Once a proposed ADR placed in the ``docs/adr`` directory has been reviewed by peers, you can either action the decision
to accept it (``pyadr accept``) or to reject it (``pyadr reject``), which will:

* Update the ADR content by:

  * Changing the ADR status (``approved`` or ``rejected``)
  * Changing the ADR date to current date

* Change the ADR file name from ``XXXX-<whatever-is-here>`` to
  ``<next-available-id>-<adr-title-in-lowercase>`` (follows
  [MADR-0005-format](https://github.com/adr/madr/blob/2.1.2/docs/adr/0005-use-dashes-in-filenames.md))

Various safety checks are performed before these actions take place. See BDD tests
in the ``features`` directory.

Installation
------------

To install ADR Process Tool, run:

.. code-block:: console

    $ pip install pyadr

Credits
-------

This package was created with Cookiecutter_ and the `opinionated-digital-center/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`opinionated-digital-center/cookiecutter-pypackage`: https://github.com/opinionated-digital-center/cookiecutter-pypackage
