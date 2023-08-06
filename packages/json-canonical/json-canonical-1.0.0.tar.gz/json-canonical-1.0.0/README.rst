JSON Canonicalizer for Python
-----------------------------

This is a Python package for a JCS (RFC 8785) compliant canonicalizer. The source code is taken from `Python2 folder from this repo <https://github.com/AnasMK/json-canonicalization>`_.

The main author of this code is `Anders Rundgren <https://github.com/cyberphone>`_. I have forked `his repo <https://github.com/cyberphone/json-canonicalization>`_ and ported Python3 code to Python 2.7. 

Installation
~~~~~~~~~~~~~~

.. code:: bash

    pip install json-canonical

Using the JSON canonicalizer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from json_canonical import canonicalize

    data = canonicalize({"tag":4})

