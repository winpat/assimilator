import pytest
from metrics import (convert_to_byte, parse_borg_create_output,
                     parse_borg_prune_output, registry)


def test_valid_convert_to_byte():

    valid_sizes = {'10 MB': 10000000,
                   '1024 kB': 1024000,
                   '321 TB': 321000000000000,
                   '234 B': 234}

    for size, solution in valid_sizes.items():

            assert convert_to_byte(size) == solution


def test_invalid_convert_to_byte():

    invalid_sizes = ['10MB', '1024KB']

    for size in invalid_sizes:

        with pytest.raises(IndexError):
            convert_to_byte(size)


def test_parse_borg_create():

    output='''------------------------------------------------------------------------------
Archive name: 20170117_121035
Archive fingerprint: 19fb854e16ee59d6e395571ae8e5178a5ab871790f05433fb7ac7ae1020839cc
Time (start): Tue, 2017-01-17 12:10:38
Time (end):   Tue, 2017-01-17 12:10:38
Duration: 0.01 seconds
Number of files: 1
------------------------------------------------------------------------------
                       Original size      Compressed size    Deduplicated size
This archive:                  840 B                969 B                555 B
All archives:                1.68 kB              1.94 kB              1.52 kB

                       Unique chunks         Total chunks
Chunk index:                       4                    6
------------------------------------------------------------------------------
'''.splitlines()


    parse_borg_create_output(output)

    test_metrics = {
        'borg_create_files_count': 1,
        'borg_create_archive_original_size_bytes': 840,
        'borg_create_archive_compressed_size_bytes': 969,
        'borg_create_archive_deduplicated_size_bytes': 555,
        'borg_create_all_archives_original_size_bytes': 1680,
        'borg_create_all_archives_compressed_size_bytes': 1940,
        'borg_create_all_archives_deduplicated_size_bytes': 1520,
        'borg_create_unique_chunks_count': 4,
        'borg_create_total_chunks_count': 6
    }

    for metric_name, solution in test_metrics.items():
        assert registry.get_sample_value(metric_name) == solution
    
    
def test_parse_borg_prune():
    output='''------------------------------------------------------------------------------
                       Original size      Compressed size    Deduplicated size
Deleted data:                 -840 B               -969 B               -555 B
All archives:                1.68 kB              1.94 kB              1.87 kB

                       Unique chunks         Total chunks
Chunk index:                       5                    6
------------------------------------------------------------------------------'''.splitlines()
    
    parse_borg_prune_output(output)

    test_metrics = {
        'borg_prune_deleted_data_original_size_bytes': -840,
        'borg_prune_deleted_data_compressed_size_bytes': -969,
        'borg_prune_deleted_data_deduplicated_size_bytes': -555,
        'borg_prune_all_archives_original_size_bytes': 1680,
        'borg_prune_all_archives_compressed_size_bytes': 1940,
        'borg_prune_all_archives_deduplicated_size_bytes': 1870,
        'borg_prune_unique_chunks_count': 5,
        'borg_prune_total_chunks_count': 6
    }

    for metric_name, solution in test_metrics.items():
        assert registry.get_sample_value(metric_name) == solution
    
