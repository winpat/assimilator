`Assimilator <http://memory-alpha.wikia.com/wiki/Assimilation>`_
===========
|travis| |license|

.. |travis| image:: https://img.shields.io/travis/winpat/assimilator.svg?style=flat-square
   :target: https://img.shields.io/github/license/winpat/assimilator.svg?style=flat-square

.. |license| image:: https://img.shields.io/github/license/winpat/assimilator.svg?style=flat-square
   :target: https://img.shields.io/github/license/winpat/assimilator.svg?style=flat-square

(Work in progress)

A wrapper around `borgbackup <https://github.com/borgbackup/borg>`_.that collects metrics and pushes them to a `Prometheus Pushgateway <https://github.com/prometheus/pushgateway>`_.

* Make borg configurable through a configuration file
* Handle the execution of preexec and postexec scripts
* Handling retention of old archives after a successful backup
* Push metrics to a `Prometheus Pushgateway <https://github.com/prometheus/pushgateway>`_
Installation
------------
1. Install python3 and pip

.. code:: shell

   apt-get install python3 python3-pip

2. Install the required python libraries

.. code:: shell

   pip3 install -r requirements.txt
  
Configuration
-------------

.. code:: yaml

    compression: none
    compression_level: 0

    paths:
      - /

    excludes:
      - /tmp
      - /proc
      - /sys

    repository: 
      user: root
      host: collective.domain.tld
      path: /var/backups/<your_repository>
      passphrase: <password>
      port: 22

    retention:
      enable: true
      hourly: 1
      daily: 1
      weekly: 1
      monthly: 1
      yearly: 1

    logging:
      level: DEBUG
      syslog: False

Prometheus Metrics
------------------

.. code:: promql

    # HELP borg_create_all_archives_compressed_size_bytes Compressed size of all archives in repository
    # TYPE borg_create_all_archives_compressed_size_bytes gauge
    borg_create_all_archives_compressed_size_bytes 2910.0
    # HELP borg_prune_return_code Exit code of borgbackup prune
    # TYPE borg_prune_return_code gauge
    borg_prune_return_code 0.0
    # HELP borg_create_all_archives_deduplicated_size_bytes Deduplicated size of all archives in repository
    # TYPE borg_create_all_archives_deduplicated_size_bytes gauge
    borg_create_all_archives_deduplicated_size_bytes 2420.0
    # HELP borg_prune_unique_chunks_count Count of unique chunks in pruned repository
    # TYPE borg_prune_unique_chunks_count gauge
    borg_prune_unique_chunks_count 5.0
    # HELP borg_prune_duration_seconds Duration of borgbackup prune
    # TYPE borg_prune_duration_seconds gauge
    borg_prune_duration_seconds 1.603191259999221
    # HELP borg_create_total_chunks_count Count of total chunks in created repository
    # TYPE borg_create_total_chunks_count gauge
    borg_create_total_chunks_count 9.0
    # HELP borg_create_return_code Exit code of borgbackup create
    # TYPE borg_create_return_code gauge
    borg_create_return_code 0.0
    # HELP borg_prune_deleted_data_original_size_bytes Original size of deleted data in pruned repository
    # TYPE borg_prune_deleted_data_original_size_bytes gauge
    borg_prune_deleted_data_original_size_bytes -840.0
    # HELP borg_create_unique_chunks_count Count of unique chunks in created repository
    # TYPE borg_create_unique_chunks_count gauge
    borg_create_unique_chunks_count 6.0
    # HELP borg_create_duration_seconds Duration of borgbackup create
    # TYPE borg_create_duration_seconds gauge
    borg_create_duration_seconds 1.5591665729998567
    # HELP borg_prune_deleted_data_compressed_size_bytes Compressed size of deleted data in pruned repository
    # TYPE borg_prune_deleted_data_compressed_size_bytes gauge
    borg_prune_deleted_data_compressed_size_bytes -969.0
    # HELP borg_create_files_count Number of transfered files
    # TYPE borg_create_files_count gauge
    borg_create_files_count 1.0
    # HELP borg_prune_deleted_data_deduplicated_size_bytes Deduplicated size of deleted data in pruned repository
    # TYPE borg_prune_deleted_data_deduplicated_size_bytes gauge
    borg_prune_deleted_data_deduplicated_size_bytes -555.0
    # HELP borg_create_archive_original_size_bytes Original size of created archive
    # TYPE borg_create_archive_original_size_bytes gauge
    borg_create_archive_original_size_bytes 840.0
    # HELP borg_prune_all_archives_original_size_bytes Original size of all archives in pruned repository
    # TYPE borg_prune_all_archives_original_size_bytes gauge
    borg_prune_all_archives_original_size_bytes 1680.0
    # HELP assimilator_preexec_return_code Exit code of assimilator preexec scripts
    # TYPE assimilator_preexec_return_code gauge
    assimilator_preexec_return_code 0.0
    # HELP borg_create_archive_compressed_size_bytes Compressed size of created archive
    # TYPE borg_create_archive_compressed_size_bytes gauge
    borg_create_archive_compressed_size_bytes 969.0
    # HELP borg_prune_all_archives_compressed_size_bytes Compressed size of all archives in pruned repository
    # TYPE borg_prune_all_archives_compressed_size_bytes gauge
    borg_prune_all_archives_compressed_size_bytes 1940.0
    # HELP assimilator_preexec_duration_seconds Duration of assimilator preexec scripts
    # TYPE assimilator_preexec_duration_seconds gauge
    assimilator_preexec_duration_seconds 0.0
    # HELP borg_create_archive_deduplicated_size_bytes Deduplicated size of created archive
    # TYPE borg_create_archive_deduplicated_size_bytes gauge
    borg_create_archive_deduplicated_size_bytes 555.0
    # HELP borg_prune_all_archives_deduplicated_size_bytes Deduplicated size of all archives in pruned repository
    # TYPE borg_prune_all_archives_deduplicated_size_bytes gauge
    borg_prune_all_archives_deduplicated_size_bytes 1870.0
    # HELP assimilator_postexec_return_code Exit code of assimilator postexec scripts
    # TYPE assimilator_postexec_return_code gauge
    assimilator_postexec_return_code 0.0
    # HELP borg_create_all_archives_original_size_bytes Original size of all archives in repository
    # TYPE borg_create_all_archives_original_size_bytes gauge
    borg_create_all_archives_original_size_bytes 2520.0
    # HELP borg_prune_total_chunks_count Count of total chunks in pruned repository
    # TYPE borg_prune_total_chunks_count gauge
    borg_prune_total_chunks_count 6.0
    # HELP assimilator_postexec_duration_seconds Duration of assimilator postexec scripts
    # TYPE assimilator_postexec_duration_seconds gauge
    assimilator_postexec_duration_seconds 0.0

Example Alerting Rules
----------------------

.. code:: promql

    TBD
    
Contributions
-------------
Contributions are more than welcome! Please feel free to open new issues or pull requests.

License
-------
GNU GENERAL PUBLIC LICENSE Version 3

See the	`LICENSE <LICENSE>`_ file.
