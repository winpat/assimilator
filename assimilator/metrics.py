#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

registry = CollectorRegistry()

PRUNE_RC = Gauge('borg_prune_exit_status', 'Exit code of borgbackup prune', registry=registry)
PRUNE_DURATION_SECONDS = Gauge('borg_prune_duration_seconds', 'Duration of borgbackup prune', registry=registry)

CREATE_RC = Gauge('borg_create_exit_status', 'Exit code of borgbackup create', registry=registry)
CREATE_DURATION_SECONDS = Gauge('borg_create_duration_seconds', 'Duration of borgbackup create', registry=registry)

PREEXEC_RC = Gauge('assimilator_preexec_exit_status', 'Exit code of assimilator preexec scripts', registry=registry)
PREEXEC_DURATION_SECONDS = Gauge('assimilator_preexec_duration_seconds', 'Duration of assimilator preexec scripts', registry=registry)

POSTEXEC_RC = Gauge('assimilator_postexec_exit_status', 'Exit code of assimilator postexec scripts', registry=registry)
POSTEXEC_DURATION_SECONDS = Gauge('assimilator_postexec_duration_seconds', 'Duration of assimilator postexec scripts', registry=registry)
