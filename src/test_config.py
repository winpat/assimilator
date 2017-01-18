import pytest
from config import validate_config, ConfigValidationError
from config import cfg

@pytest.fixture
def config():
    missing_keys = {
        'repository': {
            'passphrase': 'default'
            }
    }
    return cfg.update(missing_keys)


def test_invalid_compression_level(config):

    for level in [-1, 10, 33]:

        cfg['compression_level'] = level

        with pytest.raises(ConfigValidationError) as e:
            validate_config(cfg)
            assert e == "Invalid compression level {}".format(cfg['compression_level'])


def test_valid_compression_level(config):

    for level in [0, 6, 9]:
        cfg['compression_level'] = level
        assert validate_config(cfg) == True


def test_invalid_compression_algorithm(config):

    for algorithm in ["lz6", "lzma3"]:

        cfg['compression'] = algorithm

        with pytest.raises(ConfigValidationError) as e:
            validate_config(cfg)
            assert e == "Invalid compression algorithm {}".format(cfg['compression_level'])


def test_compression_algorithm(config):

    for algorithm in ['none', 'lz4', 'zlib', 'lzma']:
        cfg['compression'] = algorithm
        assert validate_config(cfg) == True


def test_invalid_loglevels(config):

    for level in ['INFORMATIONAL', 'DANGEROUS', 'SOMEVALUE']:

        cfg['logging']['level'] = level

        with pytest.raises(ConfigValidationError) as e:
            validate_config(cfg)
            assert e == 'Invalid log level "{}" specified'.format(cfg['logging']['level'])


def test_valid_loglevels(config):

    for level in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        cfg['logging']['level'] = level
        assert validate_config(cfg) == True



def test_valid_retention(config):

    valid_retention_configurations = [
        {'enable': True, 'hourly': 1, 'daily': 1, 'weekly': 1, 'monthly': 1, 'yearly': 1},
        {'enable': True, 'hourly': 10, 'daily': 20, 'weekly': 30, 'monthly': 40, 'yearly': 50}
    ]

    for retention in valid_retention_configurations:
        cfg['retention'] = retention
        assert validate_config(cfg) == True
