#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import check_call, CalledProcessError
from logging import handlers
from metrics import PREEXEC_DURATION_SECONDS, PREEXEC_RETURN_CODE, POSTEXEC_DURATION_SECONDS, POSTEXEC_RETURN_CODE
import logging
import argparse

logger = logging.getLogger('logger')


def parse_arguments():
    '''Parse command-line arguments'''

    parser = argparse.ArgumentParser('Wrapper around borg')

    parser.add_argument('-c', '--cfgfile', action='store',
                        metavar='CONFIG_FILE', type=str)
    parser.add_argument('-t', '--validate-configuration', action='store',
                        metavar='CONFIG_FILE', type=str)
    return parser.parse_args()


def configure_logger(level, syslog):
    '''Configure logger that will be used everywhere'''

    # TODO: Make log level configurable
    logging.basicConfig(format='%(asctime)s: [%(levelname)s] %(message)s',
                        level=logging.DEBUG)

    logger = logging.getLogger('logger')

    if syslog:
        syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
        logger.addHandler(syslog_handler)


@PREEXEC_DURATION_SECONDS.time()
def run_preexec(executables):
    '''Wrapper function to run preexec scripts
    '''
    logger.info("Running preexec scripts")
    run_executables(executables, PREEXEC_RETURN_CODE)


@POSTEXEC_DURATION_SECONDS.time()
def run_postexec(executables):
    '''Wrapper function to run postexec scripts
    '''
    logger.info("Running postexec scripts")
    run_executables(executables, POSTEXEC_RETURN_CODE)


def run_executables(executables, rcvar):

    for executable in executables:

        logger.info('Executing "%s"', executable)
        try:
            check_call([executable])          
        except CalledProcessError as e:
            logger.error('Execution failed with exception "%s"', e)
            rcvar.set(int(e.returncode))
        finally:
            break
