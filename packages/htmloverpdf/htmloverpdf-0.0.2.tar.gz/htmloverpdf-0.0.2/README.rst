===========
htmloverpdf
===========
.. image:: https://readthedocs.org/projects/htmloverpdf/badge/?version=latest
    :target: https://htmloverpdf.readthedocs.io/en/latest/?badge=latest

.. image:: https://badge.fury.io/py/htmloverpdf.svg
    :target: https://badge.fury.io/py/htmloverpdf

Render a HTML overlay over existing PDF files.

Install
-------

::

    sudo apt install libgirepository1.0-dev gir1.2-poppler-0.18 gir1.2-pango-1.0
    python3 -m pip install htmloverpdf

A wrapper for http://weasyprint.org/ which allows compositing with existing PDF files.
            
It parses the HTML looking for <img> tags with src urls ending ".pdf". Each one begins a new page and copies all source pages overlaying the weasyprint output.
The magic value "blank.pdf" outputs sections HTML without overlaying.

Usage
-----

::

    python -m htmloverpdf < test.html > test.pdf


