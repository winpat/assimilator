#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from core import run_preexec, run_postexec, parse_arguments, configure_logger
from borg import create_archive, prune_repository
from config import load_config, ConfigValidationError
from metrics import push_to_gateway, registry
import os
import logging


args = parse_arguments()

try:
    cfg = load_config(args.cfgfile)
except ConfigValidationError as e:
    os.exit(1)


configure_logger(level=cfg['logging']['level'],
                 syslog=cfg['logging']['syslog'])

logger = logging.getLogger('logger')

if 'preexec' in cfg:
    run_preexec(cfg['preexec'])

try:
    create_archive(cfg)
except RuntimeError:
    # Don't prune repository if backup creation fails.
    # Otherwise you will end up without consistent backups when you most need them.
    pass
else:
    if cfg['retention']['enable'] is True:
        prune_repository(cfg)
    else:
        logger.info('Skipping pruning of repository')

if 'postexec' in cfg:
    run_postexec(cfg['postexec'])

# The pushgateway report should be sent, even if the backups fails somewhere.
if 'pushgateway' in cfg:
    push_to_gateway('{}:{}'.format(cfg['pushgateway']['host'],
                                   cfg['pushgateway']['port']),
                    job=cfg['pushgateway']['job'], registry=registry)
    logger.info('Sent report to pushgateway')
