===========
Clustercron
===========

|pypi| |docs| |pre-commit| |workflow-ci| |codecov|

**Clustercron** is cronjob wrapper that tries to ensure that a script gets run
only once, on one host from a pool of nodes of a specified loadbalancer.
**Clustercron** select a *master* from all nodes and will run the cronjob only
on that node.

* Free software: ISC license
* Documentation: https://clustercron.readthedocs.org/en/latest/

Features
--------

Supported load balancers (till now):

    * AWS Elastic Load Balancing (ELB)
    * AWS Elastic Load Balancing v2 (ALB)


.. |pypi| image:: https://img.shields.io/pypi/v/clustercron.svg
    :alt: Pypi
    :target: https://pypi.python.org/pypi/clustercron

.. |docs| image:: https://readthedocs.org/projects/clustercron/badge/?version=latest
    :alt: Documentation Status
    :target: https://clustercron.readthedocs.io/en/latest/

.. |pre-commit| image:: https://results.pre-commit.ci/badge/github/maartenq/clustercron/main.svg
    :alt: pre-commit.ci status
    :target: https://results.pre-commit.ci/latest/github/maartenq/clustercron/main

.. |workflow-ci| image:: https://github.com/maartenq/clustercron/workflows/ci/badge.svg?branch=main
    :alt: CI status
    :target: https://github.com/maartenq/clustercron/actions?workflow=ci

.. |codecov| image:: https://codecov.io/gh/maartenq/clustercron/branch/master/graph/badge.svg?token=O0YWMFHJBG
    :alt: Codecov
    :target: https://codecov.io/gh/maartenq/clustercron
