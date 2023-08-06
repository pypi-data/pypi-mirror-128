.. image:: https://img.shields.io/pypi/v/colorconverters.svg
   :target: https://pypi.python.org/pypi/colorconverters
   :alt: PyPI Version Info
.. image:: https://img.shields.io/pypi/pyversions/colorconverters.svg
   :target: https://pypi.python.org/pypi/colorconverters
   :alt: PyPI Supported Python Versions
.. image:: https://img.shields.io/pypi/dm/colorconverters?color=blue
   :target: https://pypi.python.org/pypi/colorconverters
   :alt: PyPI downloads

A useful package which handles the utilities of converting colors to different forms.

Notable Features
----------------

- Modern pythonic syntax.
- Easy utility to convert colors to hex and vice versa.
- Easilly installable via PyPI.
- Weekly major updates.

Installing
----------

**Requires Python 3.6 or higher for desired results.**

The below codes show you how to install in various OSes

.. code:: sh

    # Windows
    py -3 -m pip install -U colorconverters

    # Linux/MacOS
    python3 -m pip install -U colorconverters

If you want to get beta and alpha versions, then install it this way instead.

.. code:: sh

    # Windows
    git clone https://github.com/ThatGenZGamer48/colorconverters
    cd colorconverters
    py -3 -m pip install -U .

    # Linux/MacOS
    git clone https://github.com/ThatGenZGamer48/colorconverters
    cd colorconverters
    python3 -m pip install -U .

Quick Example
-------------

.. code:: py

    import colorconverters
    
    # To convert to hex
    colorconverters.color_to_hex('red')

    # To convert to color
    colorconverters.hex_to_color('#FFFFFF')