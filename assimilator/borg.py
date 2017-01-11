#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from subprocess import check_call, CalledProcessError
from datetime import datetime
import logging


logger = logging.getLogger('logger')

def _compose_repository(cfg):

    return ('ssh://{}@{}:{}{}'.format(
        cfg['repository']['user'],
        cfg['repository']['host'],
        cfg['repository']['port'],
        cfg['repository']['path']
    ))


def create_archive(cfg):

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive = "{}::{}".format(_compose_repository(cfg), timestamp)

    logger.info('Creating archive "%s"'.format(timestamp))

    cmd = ["borg", "create", "--verbose", "--stats", archive]

    cmd.extend(cfg['paths'])

    if cfg['compression'] is not 'none':
        cmd.extend(['--compression', '%s,%s' %
                    (cfg['compression'],
                     cfg['compression_level'])])

    if 'exclude' in cfg:
        for exclude in cfg["excludes"]:
            cmd.extend(['--exclude', exclude])

    # print the shell equivalent for debugging purposes
    logger.debug('Composed shell command "%s"', ' '.join(cmd))

    environ["BORG_PASSPHRASE"] = cfg['repository']['passphrase']

    try:
        check_call(cmd)
    except CalledProcessError as e:
        logger.error('Creation of archive failed with exception "%s"', e)
        raise RuntimeError('Unable to create backup')


def prune_repository(cfg):
    '''Prunes a repository by removing old archive. The configuration happens
    through the retention key in the config struct
    '''

    logger.info('Pruning old archives in repository')

    cmd = ['borg', 'prune', '--verbose', '--stats']

    cmd.extend(['-H {}'.format(cfg['retention']['hourly']),
                '-d {}'.format(cfg['retention']['daily']),
                '-w {}'.format(cfg['retention']['weekly']),
                '-m {}'.format(cfg['retention']['monthly']),
                '-y {}'.format(cfg['retention']['yearly'])
    ])

    cmd.append(_compose_repository(cfg))

    print(cmd)
    logger.debug('Composed shell command "%s"', ' '.join(cmd))

    environ["BORG_PASSPHRASE"] = cfg['repository']['passphrase']

    try:
        check_call(cmd)
    except CalledProcessError as e:
        logger.error('Pruning of repository failed with exception "%s"', e)
        raise RuntimeError('Unable to prune repository')

