htmloverpdf
===========

Render a HTML overlay over existing PDF files.

A wrapper for http://weasyprint.org/ which allows compositing with existing PDF files.
            
It parses the HTML looking for <img> tags with src urls ending ".pdf". Each one begins a new page and copies all source pages overlaying the weasyprint output.
The magic value "blank.pdf" outputs sections HTML without overlaying.

Usage
-----

::

    python -m htmloverpdf < test.html > test.pdf



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   install
   htmloverpdf

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
