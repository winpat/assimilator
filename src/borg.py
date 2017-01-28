#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import environ
from subprocess import Popen, PIPE
from datetime import datetime
from metrics import (CREATE_DURATION_SECONDS, CREATE_RETURN_CODE,
                     PRUNE_DURATION_SECONDS, PRUNE_RETURN_CODE,
                     parse_borg_create_output, parse_borg_prune_output)
import logging

logger = logging.getLogger('logger')


def _compose_repository(cfg):

    return ('ssh://{}@{}:{}{}'.format(
        cfg['repository']['user'],
        cfg['repository']['host'],
        cfg['repository']['port'],
        cfg['repository']['path']
    ))


def _setup_borg_env(cfg):
    environ["BORG_PASSPHRASE"] = cfg['repository']['passphrase']
    environ["BORG_RSH"] = 'ssh -i {}'.format(cfg['identity_file'])


@CREATE_DURATION_SECONDS.time()
def create_archive(cfg):
    ''' Creates a new archive
    '''

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive = "{}::{}".format(_compose_repository(cfg), timestamp)
    cmd = ["borg", "create", "--verbose", "--list", "--stats", archive]

    cmd.extend(cfg['paths'])

    if cfg['compression'] is not 'none':
        cmd.extend(['--compression', '%s,%s' %
                    (cfg['compression'],
                     cfg['compression_level'])])

    if 'excludes' in cfg:
        for exclude in cfg["excludes"]:
            cmd.extend(['--exclude', exclude])

    # print the shell equivalent for debugging purposes
    logger.debug('Composed shell command "%s"', ' '.join(cmd))
    logger.info('Creating archive "{}"'.format(timestamp))

    _setup_borg_env(cfg)

    output = []

    # Stream output from stderr to stdout
    # http://borgbackup.readthedocs.io/en/stable/development.html#output-and-logging
    proc = Popen(cmd, stderr=PIPE, bufsize=1)
    with proc.stderr:
        for line in proc.stderr:
            line = line.decode('utf-8').strip('\n')
            print(line)
            output.append(line)

    proc.wait()

    CREATE_RETURN_CODE.set(proc.returncode)

    parse_borg_create_output(output)

    if proc.returncode is not 0:
        raise RuntimeError('Creation of archive failed with return code "{}"'.format(proc.returncode))


@PRUNE_DURATION_SECONDS.time()
def prune_repository(cfg):
    '''Prunes a repository by removing old archives.

    The configuration happens through the retention key in the config struct

    '''

    cmd = ['borg', 'prune', '--verbose', '--list', '--stats']

    retention_contraints = [{'flag': '--keep-hourly', 'name': 'hourly'},
                            {'flag': '--keep-daily', 'name': 'daily'},
                            {'flag': '--keep-weekly', 'name': 'weekly'},
                            {'flag': '--keep-monthly', 'name': 'monthly'},
                            {'flag': '--keep-yearly', 'name': 'yearly'}]

    for constraint in retention_contraints:
        try:
            cmd.extend([constraint['flag'], str(cfg['retention'][constraint['name']])])
        except KeyError:
            pass

    cmd.append(_compose_repository(cfg))

    logger.info('Pruning old archives in repository')
    logger.debug('Composed shell command "%s"', ' '.join(cmd))


    _setup_borg_env(cfg)

    output = []
    # Stream output from stderr to stdout
    # http://borgbackup.readthedocs.io/en/stable/development.html#output-and-logging
    proc = Popen(cmd, stderr=PIPE, bufsize=1)
    with proc.stderr:
        for line in proc.stderr:
            line = line.decode('utf-8').strip('\n')
            print(line)
            output.append(line)

    proc.wait()

    PRUNE_RETURN_CODE.set(proc.returncode)

    parse_borg_prune_output(output)

    if proc.returncode is not 0:
        raise RuntimeError('Pruning of repository failed with return code "{}"'.format(proc.returncode))
