import pytest
from metrics import convert_to_byte


def test_valid_convert_to_byte():

    valid_sizes = {'10 MB': 10000000,
                   '1024 kB': 1024000,
                   '321 TB': 321000000000000}

    for size, solution in valid_sizes.items():

            assert convert_to_byte(size) == solution


def test_invalid_convert_to_byte():

    invalid_sizes = ['10MB', '1024KB']

    for size in invalid_sizes:

        with pytest.raises(IndexError):
            convert_to_byte(size)

# TODO: Write unit test for `parse_borg_create_output()`
# TODO: Write unit test for `parse_borg_create_prune()`
