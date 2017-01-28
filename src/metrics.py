#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prometheus_client import CollectorRegistry, Gauge
import re


registry = CollectorRegistry()

ASSIMILATOR_RETURN_CODE = Gauge('assimilator_return_code',
                                'Exit code of assimilator',
                                registry=registry)
PREEXEC_RETURN_CODE = Gauge('assimilator_preexec_return_code',
                            'Exit code of assimilator preexec scripts',
                            registry=registry)

PREEXEC_DURATION_SECONDS = Gauge('assimilator_preexec_duration_seconds',
                                 'Duration of assimilator preexec scripts',
                                 registry=registry)

POSTEXEC_RETURN_CODE = Gauge('assimilator_postexec_return_code',
                             'Exit code of assimilator postexec scripts',
                             registry=registry)

POSTEXEC_DURATION_SECONDS = Gauge('assimilator_postexec_duration_seconds',
                                  'Duration of assimilator postexec scripts',
                                  registry=registry)

PRUNE_RETURN_CODE = Gauge('borg_prune_return_code',
                          'Exit code of borgbackup prune',
                          registry=registry)

PRUNE_DURATION_SECONDS = Gauge('borg_prune_duration_seconds',
                               'Duration of borgbackup prune',
                               registry=registry)

PRUNE_DELETED_DATA_ORIGINAL_SIZE_BYTES = Gauge('borg_prune_deleted_data_original_size_bytes',
                           'Original size of deleted data in pruned repository',
                           registry=registry)

PRUNE_DELETED_DATA_COMPRESSED_SIZE_BYTES = Gauge('borg_prune_deleted_data_compressed_size_bytes',
                           'Compressed size of deleted data in pruned repository',
                           registry=registry)

PRUNE_DELETED_DATA_DEDUPLICATED_SIZE_BYTES = Gauge('borg_prune_deleted_data_deduplicated_size_bytes',
                           'Deduplicated size of deleted data in pruned repository',
                           registry=registry)

PRUNE_ALL_ARCHIVES_ORIGINAL_SIZE_BYTES = Gauge('borg_prune_all_archives_original_size_bytes',
                                               'Original size of all archives in pruned repository',
                                               registry=registry)

PRUNE_ALL_ARCHIVES_COMPRESSED_SIZE_BYTES = Gauge('borg_prune_all_archives_compressed_size_bytes',
                                                 'Compressed size of all archives in pruned repository',
                                                 registry=registry)

PRUNE_ALL_ARCHIVES_DEDUPLICATED_SIZE_BYTES = Gauge('borg_prune_all_archives_deduplicated_size_bytes',
                                                   'Deduplicated size of all archives in pruned repository',
                                                   registry=registry)

PRUNE_TOTAL_CHUNKS_COUNT = Gauge('borg_prune_total_chunks_count',
                                  'Count of total chunks in pruned repository',
                                  registry=registry)

PRUNE_UNIQUE_CHUNKS_COUNT = Gauge('borg_prune_unique_chunks_count',
                                   'Count of unique chunks in pruned repository',
                                   registry=registry)

CREATE_RETURN_CODE = Gauge('borg_create_return_code',
                           'Exit code of borgbackup create',
                           registry=registry)

CREATE_DURATION_SECONDS = Gauge('borg_create_duration_seconds',
                                'Duration of borgbackup create',
                                registry=registry)

CREATE_FILES_COUNT = Gauge('borg_create_files_count',
                           'Number of transfered files',
                           registry=registry)

CREATE_ARCHIVE_ORIGINAL_SIZE_BYTES = Gauge('borg_create_archive_original_size_bytes',
                                           'Original size of created archive',
                                           registry=registry)

CREATE_ARCHIVE_COMPRESSED_SIZE_BYTES = Gauge('borg_create_archive_compressed_size_bytes',
                                             'Compressed size of created archive',
                                             registry=registry)

CREATE_ARCHIVE_DEDUPLICATED_SIZE_BYTES = Gauge('borg_create_archive_deduplicated_size_bytes',
                                               'Deduplicated size of created archive',
                                               registry=registry)

CREATE_ALL_ARCHIVES_ORIGINAL_SIZE_BYTES = Gauge('borg_create_all_archives_original_size_bytes',
                                                'Original size of all archives in repository',
                                                registry=registry)

CREATE_ALL_ARCHIVES_COMPRESSED_SIZE_BYTES = Gauge('borg_create_all_archives_compressed_size_bytes',
                                                  'Compressed size of all archives in repository',
                                                  registry=registry)

CREATE_ALL_ARCHIVES_DEDUPLICATED_SIZE_BYTES = Gauge('borg_create_all_archives_deduplicated_size_bytes',
                                                    'Deduplicated size of all archives in repository',
                                                    registry=registry)

CREATE_TOTAL_CHUNKS_COUNT = Gauge('borg_create_total_chunks_count',
                                  'Count of total chunks in created repository',
                                  registry=registry)

CREATE_UNIQUE_CHUNKS_COUNT = Gauge('borg_create_unique_chunks_count',
                                   'Count of unique chunks in created repository',
                                   registry=registry)


def _trim_borg_output(output):
    ''' Returns borg backup output trimed of unrequired lines.

    The `borg create` output will contain all transfered files and
    directories, as well as information about the progress of the current
    file transfer.

    Because the count of transfered files varies from run to run it has to
    be cut away.
    '''

    sentinel_index = output.index("------------------------------------------------------------------------------")
    return output[sentinel_index:]


def parse_borg_create_output(output):
    '''Parse `borg create` output and extract various metrics
    '''

    output = _trim_borg_output(output)

    # Parse "Number of files:" section
    pattern = re.compile('Number of files: ([0-9]*)')
    match = re.match(pattern, output[6])
    CREATE_FILES_COUNT.set(match.group(1))

    # Parse "This archives:" section
    pattern = re.compile('This archive:\s*([0-9.]*\s[kBMGTEZY]{1,2})\s*([0-9.]*\s[kBMGTEZY]{1,2})\s*([0-9.]*\s[kBMGTEZY]{1,2})')
    match = re.match(pattern, output[9])
    CREATE_ARCHIVE_ORIGINAL_SIZE_BYTES.set(convert_to_byte(match.group(1)))
    CREATE_ARCHIVE_COMPRESSED_SIZE_BYTES.set(convert_to_byte(match.group(2)))
    CREATE_ARCHIVE_DEDUPLICATED_SIZE_BYTES.set(convert_to_byte(match.group(3)))

    # Parse "All archives:" section
    pattern = re.compile('All archives:\s*([0-9.]*\s[kBMGTEZY]{1,2})\s*([0-9.]*\s[kBMGTEZY]{1,2})\s*([0-9.]*\s[kBMGTEZY]{1,2})')
    match = re.match(pattern, output[10])
    CREATE_ALL_ARCHIVES_ORIGINAL_SIZE_BYTES.set(convert_to_byte(match.group(1)))
    CREATE_ALL_ARCHIVES_COMPRESSED_SIZE_BYTES.set(convert_to_byte(match.group(2)))
    CREATE_ALL_ARCHIVES_DEDUPLICATED_SIZE_BYTES.set(convert_to_byte(match.group(3)))

    # Parse "Chunk index:" section
    pattern = re.compile('Chunk index:\s*([0-9]*)\s*([0-9]*)')
    match = re.match(pattern, output[13])
    CREATE_UNIQUE_CHUNKS_COUNT.set(match.group(1))
    CREATE_TOTAL_CHUNKS_COUNT.set(match.group(2))


def parse_borg_prune_output(output):
    '''Parse `borg prune` output and extract various metrics
    '''

    output = _trim_borg_output(output)

    # Parse "Deleted data:" section
    pattern = re.compile('Deleted data:\s*([\-0-9.]*\s[kBMGTEZY]{1,2})\s*([\-0-9.]*\s[kBMGTEZY]{1,2})\s*([\-0-9.]*\s[kBMGTEZY]{1,2})')
    match = re.match(pattern, output[2])
    PRUNE_DELETED_DATA_ORIGINAL_SIZE_BYTES.set(convert_to_byte(match.group(1)))
    PRUNE_DELETED_DATA_COMPRESSED_SIZE_BYTES.set(convert_to_byte(match.group(2)))
    PRUNE_DELETED_DATA_DEDUPLICATED_SIZE_BYTES.set(convert_to_byte(match.group(3)))

    # Parse "All archives:" section
    pattern = re.compile('All archives:\s*([0-9.]*\s[kBMGTEZY]{1,2})\s*([0-9.]*\s[kBMGTEZY]{1,2})\s*([0-9.]*\s[kBMGTEZY]{1,2})')
    match = re.match(pattern, output[3])
    PRUNE_ALL_ARCHIVES_ORIGINAL_SIZE_BYTES.set(convert_to_byte(match.group(1)))
    PRUNE_ALL_ARCHIVES_COMPRESSED_SIZE_BYTES.set(convert_to_byte(match.group(2)))
    PRUNE_ALL_ARCHIVES_DEDUPLICATED_SIZE_BYTES.set(convert_to_byte(match.group(3)))

    # Parse "Chunk index:" section
    pattern = re.compile('Chunk index:\s*([0-9]*)\s*([0-9]*)')
    match = re.match(pattern, output[6])
    PRUNE_UNIQUE_CHUNKS_COUNT.set(match.group(1))
    PRUNE_TOTAL_CHUNKS_COUNT.set(match.group(2))


def convert_to_byte(size):
    ''' Takes a value with it binary prefix and converts it to raw bytes.

    For further reference checkout https://en.wikipedia.org/wiki/Binary_prefix
    '''

    size = size.split(" ")
    unit = size[1]
    value = size[0]

    switcher = {
        'B' : 1000**0,
        'kB': 1000**1,
        'MB': 1000**2,
        'GB': 1000**3,
        'TB': 1000**4,
        'PB': 1000**5,
        'EB': 1000**6,
        'ZB': 1000**7,
        'YB': 1000**8
    }

    # 4 th function from switcher dictionary
    return float(value) * switcher.get(unit)


def calculate_return_code():

    rc = 0

    for rc_var in ['PREEXEC_RETURN_CODE', 'POSTEXEC_RETURN_CODE',
                   'CREATE_RETURN_CODE', 'PRUNE_RETURN_CODE']:
        if registry.get_sample_value(rc_var) is not 0:
            rc = 1

    ASSIMILATOR_RETURN_CODE.set(rc)
    return rc
