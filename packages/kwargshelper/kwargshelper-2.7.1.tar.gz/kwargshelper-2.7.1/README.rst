Welcome to kwargs’s docs!
=========================

|codecov| |gws| |lic| |pver| |pwheel| |github|

kwargshelper
------------

A python package for working with **kwargs**.

Allows for validation of args passed in via ``**kwargs`` in various ways.
Such as type checking, rules checking, error handeling.

Many built in rules that make validation of input simple and effective.
Easily create and add new rules.

Various callbacks to hook each **kwarg** with rich set of options for fine control.

Docs
++++

Read the docs `here <https://python-kwargshelper.readthedocs.io/>`_

Installation
++++++++++++

You can install the Version Class from `PyPI <https://pypi.org/project/kwargshelper/>`_

.. code-block:: bash

    pip install kwargshelper

KwargsHelper Class
++++++++++++++++++

Helper class for working with python ``**kwargs`` in a class constructor

Assigns values of ``**kwargs`` to an exising class with type checking and rules

Parse kwargs with suport for rules that can be extended that validate any arg of kwargs.
Type checking of any type.

Callback function for before update that includes a Cancel Option.

Many other options avaliable for more complex usage.

KwArg Class
+++++++++++

Helper class for working with python ``**kwargs`` in a method/function
Wrapper for ``KwargsHelper`` Class.

Assigns values of ``**kwargs`` to itself with validation

Parse kwargs with suport for rules that can be extended that validate any arg of kwargs.
Type checking of any type.

Callback function for before update that includes a Cancel Option.

Many other options avaliable for more complex usage.

Decorator Classes
+++++++++++++++++

Decorators that can applied to function that validate arguments.

Decorators for Type checking and Rule testing is built in.

The following example ensures all function args are a positive ``int`` or a positive ``float``.

.. code-block:: python

    from kwhelp.decorator import RuleCheckAny
    import kwhelp.rules as rules

    @RuleCheckAny(rules.RuleIntPositive, rules.RuleFloatPositive)
    def speed_msg(speed, limit, **kwargs) -> str:
        if limit > speed:
            msg = f"Current speed is '{speed}'. You may go faster as the limit is '{limit}'."
        elif speed == limit:
            msg = f"Current speed is '{speed}'. You are at the limit."
        else:
            msg = f"Please slow down limit is '{limit}' and you are currenlty going '{speed}'."
        if 'hours' in kwargs:
            msg = msg + f" Current driving hours is '{kwargs['hours']}'"
        return msg

.. |codecov| image:: https://codecov.io/gh/Amourspirit/python-kwargshelper/branch/master/graph/badge.svg?token=mJ2HdGwSGy
    :target: https://codecov.io/gh/Amourspirit/python-kwargshelper
    :alt: codecov

.. |gws| image:: https://img.shields.io/github/workflow/status/Amourspirit/python-kwargshelper/CodeCov
    :alt: GitHub Workflow Status

.. |lic| image:: https://img.shields.io/github/license/Amourspirit/python-kwargshelper
    :alt: License MIT

.. |pver| image:: https://img.shields.io/pypi/pyversions/kwargshelper
    :alt: PyPI - Python Version

.. |pwheel| image:: https://img.shields.io/pypi/wheel/kwargshelper
    :alt: PyPI - Wheel

.. |github| image:: https://img.shields.io/badge/GitHub-100000?style=plastic&logo=github&logoColor=white
    :target: https://github.com/Amourspirit/python-kwargshelper
    :alt: Github