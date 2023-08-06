==========
user_agent
==========

.. image:: https://travis-ci.org/lorien/user_agent.png?branch=master
    :target: https://travis-ci.org/lorien/user_agent?branch=master

.. image:: https://ci.appveyor.com/api/projects/status/jbyd2b9dfq99fvs3
    :target: https://ci.appveyor.com/project/lorien/user-agent

.. image:: https://readthedocs.org/projects/user_agent/badge/?version=latest
    :target: http://user-agent.readthedocs.org


What is user_agent module for?
-------------------------------

This module is for generating random, valid web user agents:

* content of "User-Agent" HTTP headers



Usage Example
-------------

.. code:: python

    >>> from useragent_rs import *
    >>> s=getSO()
    >>> print ('SO supported ', s)
    SO supported  ['Windows', 'Linux', 'macOS', 'OpenBSD', 'Android', 'Mac OS X', 'iOS', 'Chrome OS', 'FreeBSD']

    >>> s=getBrowserType()
    >>> print ('Browser supported ', s)
    Browser supported  ['Chrome', 'Opera']

    >>> s=getBrowserType()
    >>> print ('Browser supported ', s)
    Browser supported  ['Chrome', 'Opera']


    >>> h=getHardwareType()
    >>> print ('HW supported ', h)
    HW supported  ['Computer', 'Mobile', 'Mobile - Phone', 'Large Screen - TV']

    >>> a=getUserAgent()
    >>> print(a)
    [{'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3972.146 Safari/537.36 OPR/53.0.4161.46', 'version': 53, 'so': 'Windows', 'hardwareType': 'Computer', 'browser': 'Opera'}]

    >>> a=getUserAgentForSO('Windows')
    >>> print(a)
    [{'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3972.146 Safari/537.36 OPR/53.0.4161.46', 'version': 53, 'so': 'Windows', 'hardwareType': 'Computer', 'browser': 'Opera'}]

    >>> a=getUserAgentForSO()
    >>> print(a)
    [{'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3972.146 Safari/537.36 OPR/53.0.4161.46', 'version': 53, 'so': 'Windows', 'hardwareType': 'Computer', 'browser': 'Opera'}]

    >>> a=getUserAgentForHW('Computer')
    >>> print(a)
    [{'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3972.146 Safari/537.36 OPR/53.0.4161.46', 'version': 53, 'so': 'Windows', 'hardwareType': 'Computer', 'browser': 'Opera'}]

    >>> a=getUserAgentForHW()
    >>> print(a)
    [{'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3972.146 Safari/537.36 OPR/53.0.4161.46', 'version': 53, 'so': 'Windows', 'hardwareType': 'Computer', 'browser': 'Opera'}]

    >>> a=getUserAgentForBrowser('Opera')
    >>> print(a)
    [{'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3972.146 Safari/537.36 OPR/53.0.4161.46', 'version': 53, 'so': 'Windows', 'hardwareType': 'Computer', 'browser': 'Opera'}]

    >>> a=getUserAgentForBrowser()
    >>> print(a)
    [{'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3972.146 Safari/537.36 OPR/53.0.4161.46', 'version': 53, 'so': 'Windows', 'hardwareType': 'Computer', 'browser': 'Opera'}]


Installation
------------

.. code:: shell

    $ pip install -U useragent_rs



