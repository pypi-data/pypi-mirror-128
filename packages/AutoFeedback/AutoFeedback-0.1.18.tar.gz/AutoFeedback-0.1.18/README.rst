================================
AutoFeedback: Assignment Checker
================================

.. image:: https://img.shields.io/travis/abrown41/AutoFeedback.svg
        :target: https://travis-ci.org/abrown41/AutoFeedback

.. image:: https://img.shields.io/pypi/v/AutoFeedback.svg
        :target: https://pypi.python.org/pypi/AutoFeedback


check basic python exercises with pretty feedback

* Free software: 3-clause BSD license
* Documentation: (COMING SOON!) https://abrown41.github.io/AutoFeedback.

===========
Description
===========
AutoFeedback is a suite of python utilities for testing and providing usable feedback introductory python assignments, specifically relevant to mathematics and the use of numpy and matplotlib.

=======================
How to use AutoFeedback
=======================

AutoFeedback can be installed via pip

    pip install AutoFeedback

The suite provides three basic checkers: one each for checking variables,
functions and matplotlib.pyplot figures. 

===========================================
Installing a local version of AutoFeedback
===========================================

If you want to develop AutoFeedback you can install a local version of the code.  You can then create a local wheel file by running the command:

python setup.py sdist bdist_wheel

The whl file to install AutoFeedback is then created in a directory called `dist`.  To install your version of AutoFeedback in place of the default you then do:

pip uninstall AutoFeedback
pip install dist/AutoFeedback-<version>-py3-none-any.whl
