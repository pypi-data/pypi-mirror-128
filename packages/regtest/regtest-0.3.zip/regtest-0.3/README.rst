
Regression test enhancement for the Python *unittest* framework

.. image:: https://img.shields.io/codeship/a5a60730-ba8a-0137-8179-0660bd8c08b8/master.svg
   :target: https://codeship.com//projects/364831
   :alt: Codeship

.. image:: https://img.shields.io/readthedocs/regtest
   :target: http://regtest.readthedocs.io
   :alt: Read the Docs

.. image:: https://img.shields.io/github/license/sonntagsgesicht/regtest
   :target: https://github.com/sonntagsgesicht/regtest/raw/master/LICENSE
   :alt: GitHub

.. image:: https://img.shields.io/github/release/sonntagsgesicht/regtest?label=github
   :target: https://github.com/sonntagsgesicht/regtest/releases
   :alt: GitHub release

.. image:: https://img.shields.io/pypi/v/regtest
   :target: https://pypi.org/project/regtest/
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/regtest
   :target: https://pypi.org/project/regtest/
   :alt: PyPI - Python Version

.. image:: https://pepy.tech/badge/regtest
   :target: https://pypi.org/project/regtest/
   :alt: PyPI Downloads


Writing tests is important
(see `here <https://auxilium.readthedocs.io/en/latest/intro.html>`_).
And when it comes to an existing and running application even more.
Existing results must at any chance be reproduced (*like-for-like* tests).

An easy way to add many test cases
is by invoking the application and its subroutines many times.
But taking notes (and hardcoding) of all results is annoying.

Here **regtest** might help.

Simply, write routines that invoke our application.
The initial run will collect and store return values in files.
The next time (and at any time these routines run) the return values
will be checked against the stored ones.

To reset a routine simply remove the corresponding file
(named accordingly) of stored reference data.
The next time the reference data will be rebuild.

