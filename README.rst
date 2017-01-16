`Assimilator <http://memory-alpha.wikia.com/wiki/Assimilation>`_
===========

(Work in progress)

A wrapper around borgbackup that collects metrics and pushes them to a Prometheus Pushgateway.

* Makes borgbackup configurable through a configuration file
* Hande the execution of preexec and postexec scripts
* Handling retention of old archives after a successful backup
* Push metrics to a `Prometheus Pushgateway <https://github.com/prometheus/pushgateway>`_
Installation
------------
1. Install the dependencies

.. code:: shell

   apt-get install python3 python3-pip

2. Install the prometheus client library

.. code:: shell

   pip3 install -r requirements.txt

Prometheus Metrics
------------------

.. code:: promql

    # HELP assimilator_create_return_code Exit code of borgbackup create
    # TYPE assimilator_create_return_code gauge
    assimilator_create_return_code 0.0
    # HELP assimilator_create_total_chunks Total chunks of created archive
    # TYPE assimilator_create_total_chunks gauge
    assimilator_create_total_chunks 24.0
    # HELP assimilator_create_duration_seconds Duration of borgbackup create
    # TYPE assimilator_create_duration_seconds gauge
    assimilator_create_duration_seconds 1.7372676710001542
    # HELP assimilator_create_unique_chunks Unique chunks of created archive
    # TYPE assimilator_create_unique_chunks gauge
    assimilator_create_unique_chunks 10.0
    # HELP assimilator_create_files_count Number of transfered files
    # TYPE assimilator_create_files_count gauge
    assimilator_create_files_count 1.0
    # HELP assimilator_archive_original_size_bytes Original size of created archive
    # TYPE assimilator_archive_original_size_bytes gauge
    assimilator_archive_original_size_bytes 840.0
    # HELP assimilator_archive_compressed_size_bytes Compressed size of created archive
    # TYPE assimilator_archive_compressed_size_bytes gauge
    assimilator_archive_compressed_size_bytes 969.0
    # HELP borg_prune_duration_seconds Duration of borgbackup prune
    # TYPE borg_prune_duration_seconds gauge
    borg_prune_duration_seconds 1.7606788160001088
    # HELP assimilator_archive_deduplicated_size_bytes Deduplicated size of created archive
    # TYPE assimilator_archive_deduplicated_size_bytes gauge
    assimilator_archive_deduplicated_size_bytes 555.0
    # HELP assimilator_preexec_return_code Exit code of assimilator preexec scripts
    # TYPE assimilator_preexec_return_code gauge
    assimilator_preexec_return_code 0.0
    # HELP assimilator_all_archives_original_size_bytes Original size of all archives in repository
    # TYPE assimilator_all_archives_original_size_bytes gauge
    assimilator_all_archives_original_size_bytes 6720.0
    # HELP assimilator_preexec_duration_seconds Duration of assimilator preexec scripts
    # TYPE assimilator_preexec_duration_seconds gauge
    assimilator_preexec_duration_seconds 0.0
    # HELP borg_prune_return_code Exit code of borgbackup prune
    # TYPE borg_prune_return_code gauge
    borg_prune_return_code 0.0
    # HELP assimilator_all_archives_compressed_size_bytes Compressed size of all archives in repository
    # TYPE assimilator_all_archives_compressed_size_bytes gauge
    assimilator_all_archives_compressed_size_bytes 7750.0
    # HELP assimilator_postexec_return_code Exit code of assimilator postexec scripts
    # TYPE assimilator_postexec_return_code gauge
    assimilator_postexec_return_code 0.0
    # HELP assimilator_all_archives_deduplicated_size_bytes Deduplicated size of all archives in repository
    # TYPE assimilator_all_archives_deduplicated_size_bytes gauge
    assimilator_all_archives_deduplicated_size_bytes 4850.0
    # HELP assimilator_postexec_duration_seconds Duration of assimilator postexec scripts
    # TYPE assimilator_postexec_duration_seconds gauge
    assimilator_postexec_duration_seconds 0.0

Example Alerting Rules
----------------------

.. code:: promql

    TBD
  
