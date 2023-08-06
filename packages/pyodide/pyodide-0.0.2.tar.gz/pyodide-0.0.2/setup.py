from setuptools import setup

import sys

if not (len(sys.argv) >= 2 and sys.argv[:2] == ['setup.py', 'sdist']):
    # Anything else than running `setup.py sdist` should fail
    raise ValueError(
        'Pyodide is a Python distribution that runs in the browser '
        'or Node.js. It cannot be installed from PyPi.\n'
        '            See https://github.com/pyodide/pyodide '
        'for how to use Pyodide.')

setup()
