#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prometheus_client import CollectorRegistry, Gauge
import re


registry = CollectorRegistry()

PRUNE_RETURN_CODE = Gauge('borg_prune_return_code',
                 'Exit code of borgbackup prune',
                 registry=registry)

PRUNE_DURATION_SECONDS = Gauge('borg_prune_duration_seconds',
                               'Duration of borgbackup prune',
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

CREATE_RETURN_CODE = Gauge('assimilator_create_return_code',
                           'Exit code of borgbackup create',
                           registry=registry)

CREATE_DURATION_SECONDS = Gauge('assimilator_create_duration_seconds',
                                'Duration of borgbackup create',
                                registry=registry)

CREATE_FILES_COUNT = Gauge('assimilator_create_files_count',
                           'Number of transfered files',
                           registry=registry)

CREATE_ARCHIVE_ORIGINAL_SIZE_BYTES = Gauge('assimilator_archive_original_size_bytes',
                                           'Original size of created archive',
                                           registry=registry)

CREATE_ARCHIVE_COMPRESSED_SIZE_BYTES = Gauge('assimilator_archive_compressed_size_bytes',
                                             'Compressed size of created archive',
                                             registry=registry)

CREATE_ARCHIVE_DEDUPLICATED_SIZE_BYTES = Gauge('assimilator_archive_deduplicated_size_bytes',
                                               'Deduplicated size of created archive',
                                               registry=registry)

CREATE_ALL_ARCHIVES_ORIGINAL_SIZE_BYTES = Gauge('assimilator_all_archives_original_size_bytes',
                                                'Original size of all archives in repository',
                                                registry=registry)

CREATE_ALL_ARCHIVES_COMPRESSED_SIZE_BYTES = Gauge('assimilator_all_archives_compressed_size_bytes',
                                                  'Compressed size of all archives in repository',
                                                  registry=registry)

CREATE_ALL_ARCHIVES_DEDUPLICATED_SIZE_BYTES = Gauge('assimilator_all_archives_deduplicated_size_bytes',
                                                    'Deduplicated size of all archives in repository',
                                                    registry=registry)

CREATE_TOTAL_CHUNKS_COUNT = Gauge('assimilator_create_total_chunks',
                                  'Total chunks of created archive',
                                  registry=registry)

CREATE_UNIQUE_CHUNKS_COUNT = Gauge('assimilator_create_unique_chunks',
                                   'Unique chunks of created archive',
                                   registry=registry)


def parse_borg_create_output(output):
    '''Parse `borg create` output and extract various metrics
    '''

    # Parse "Number of files:" section
    pattern = re.compile('Number of files: ([0-9]*)')
    match = re.match(pattern, output[6])
    CREATE_FILES_COUNT.set(match.group(1))

    # Parse "This archives:" section
    pattern = re.compile('This archive:\s*([0-9.]*\s[kBMGTEZY]{2})\s*([0-9.]*\s[kBMGTEZY]{2})\s*([0-9.]*\s[kBMGTEZY]{2})')
    match = re.match(pattern, output[9])
    CREATE_ARCHIVE_ORIGINAL_SIZE_BYTES.set(convert_to_byte(match.group(1)))
    CREATE_ARCHIVE_COMPRESSED_SIZE_BYTES.set(convert_to_byte(match.group(2)))
    CREATE_ARCHIVE_DEDUPLICATED_SIZE_BYTES.set(convert_to_byte(match.group(3)))

    # Parse "All archives:" section
    pattern = re.compile('All archives:\s*([0-9.]*\s[kBMGTEZY]{2})\s*([0-9.]*\s[kBMGTEZY]{2})\s*([0-9.]*\s[kBMGTEZY]{2})')
    match = re.match(pattern, output[10])
    CREATE_ALL_ARCHIVES_ORIGINAL_SIZE_BYTES.set(convert_to_byte(match.group(1)))
    CREATE_ALL_ARCHIVES_COMPRESSED_SIZE_BYTES.set(convert_to_byte(match.group(2)))
    CREATE_ALL_ARCHIVES_DEDUPLICATED_SIZE_BYTES.set(convert_to_byte(match.group(3)))

    # Parse "Chunk index:" section
    pattern = re.compile('Chunk index:\s*([0-9]*)\s*([0-9]*)')
    match = re.match(pattern, output[13])
    CREATE_UNIQUE_CHUNKS_COUNT.set(match.group(1))
    CREATE_TOTAL_CHUNKS_COUNT.set(match.group(2))


def convert_to_byte(size):
    ''' Takes a value with it binary prefix (https://en.wikipedia.org/wiki/Binary_prefix) 
    and converts it to raw bytes.
    '''

    size = size.split(" ")
    unit = size[1]
    value = size[0]

    switcher = {
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
