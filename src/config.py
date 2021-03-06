#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from yaml import load
import logging
import os


log = logging.getLogger('logger')

# Sane default values for optional configuration parameters
cfg = {
    'compression': 'none',
    'compression_level': 6,
    'checkpoint_interval': 300,
    'paths': ['/'],
    'repository': {
        'user': 'root',
        'host': '127.0.0.1',
        'port': '22',
        'path': '/',
    },
    'logging': {
        'level': 'DEBUG',
        'file': '',
        'syslog': True,
    },
    'retention': {
        'enable': False,
    }
}


class ConfigValidationError(Exception):
    pass


def load_config(file):
    'Parses a yaml config file and validates the config'

    log.info('Parsing configuration file "%s"', file)

    with open(file, 'r') as ymlfile:
        cfg.update(load(ymlfile))

    log.debug('Successfully parsed and validated config file: "%s"', repr(cfg))

    validate_config(cfg)

    return cfg


def validate_config(cfg):
    '''Validates config dictionary to catch configuration errors early on runtime.
       Prevent configuration to corrupt existing backups.
    '''

    if cfg['compression'] not in ['none', 'lz4', 'zlib', 'lzma']:
        raise ConfigValidationError('Invalid compression algorithm specified "{}"'
                                    .format(cfg['compression']))

    if cfg['compression_level'] not in range(10):
        raise ConfigValidationError('Invalid compression level specified "{}"'
                                    .format(cfg['compression_level']))

    for path in cfg['paths']:
        if not os.path.exists(path):
                raise ConfigValidationError('Invalid backup path specified "{}"'.format(path))

    if not cfg['repository']['passphrase']:
        raise ConfigValidationError('No repository passphrase specified')

    if cfg['logging']['level'] not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ConfigValidationError('Invalid log level "{}" specified'
                                    .format(cfg['logging']['level']))

    if not os.access(cfg['identity_file'], os.R_OK):
        raise ConfigValidationError('SSH identity file "{}" is not readable'.format(cfg['identity_file']))

    if 'postexec' in cfg:
        for executable in cfg["postexec"]:
            if not os.access(executable, os.X_OK):
                raise ConfigValidationError('Postexec script "{}" is not executable'.format(executable))

    if 'preexec' in cfg:
        for executable in cfg["preexec"]:
            if not os.access(executable, os.X_OK):
                raise ConfigValidationError('Postexec script "{}" is not executable'.format(executable))

    if cfg['retention']['enable'] is True:
        _validate_retention_config(cfg)

    return True


def _validate_retention_config(cfg):

    valid_retention_keys = ['hourly', 'daily', 'weekly', 'monthly', 'yearly']

    for item in valid_retention_keys:
        try:
            if cfg['retention'][item] < 1:
                raise ConfigValidationError('Invalid retention time "{}" for "{}"'
                                            .format(cfg['retention'][item], item))

        except KeyError:
            # If retention is enabled at least one constraint is required (hourly, daily...)

            # Check of intersections
            if len(set(valid_retention_keys) & set(list(cfg['retention'].keys()))) < 1:
                raise ConfigValidationError('No valid retention constraints found in configuration. Please specify at least one (hourly, daily...)')
