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

    for level in  [-1, 10, 33]:
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

def test_valid_compression_algorithm(config):

    for algorithm in ['none', 'lz4', 'zlib', 'lzma']:
        cfg['compression'] = algorithm
        assert validate_config(cfg) == True
