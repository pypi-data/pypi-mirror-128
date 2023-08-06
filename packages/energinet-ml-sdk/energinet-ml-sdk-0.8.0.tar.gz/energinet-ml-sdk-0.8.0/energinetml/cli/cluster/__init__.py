#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""[summary]
"""
import click

from .change import change as change_cluster
from .create import create as create_cluster


@click.group()
def cluster_group() -> None:
    """Manage compute clusters for a model."""
    pass


cluster_group.add_command(create_cluster)
cluster_group.add_command(change_cluster)
