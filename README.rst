Assimilator
===========
A wrapper around borgbackup which:

* Makes borgbackup configurable through a configuration file
* Hande the execution of preexec and postexec scripts
* Handling retention after a successful backup
* Push metrics to a Prometheus Pushgateway


Installation
------------
1. Install the requirements

.. code:: shell
   apt-get install python3 python3-yaml python3-pip
