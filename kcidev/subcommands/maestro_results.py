#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from git import Repo

from kcidev.libs.common import *
from kcidev.libs.maestro_common import *


@click.command(
    help="""Query test results from KernelCI's Maestro API.

This command allows you to retrieve test results either by specific node ID
or by fetching the latest nodes with pagination and filtering options.

\b
Examples:
  kci-dev maestro-results --nodeid <NODE_ID>
  kci-dev maestro-results --nodes --limit 10
  kci-dev maestro-results --nodes --filter "status=fail"
  kci-dev maestro-results --nodes --field name --field status
"""
)
@click.option(
    "--nodeid",
    required=False,
    help="Retrieve results for a specific node ID",
)
@click.option(
    "--nodes",
    is_flag=True,
    required=False,
    help="Retrieve the latest test node results",
)
@click.option(
    "--limit",
    default=50,
    required=False,
    help="Maximum number of nodes to retrieve (default: 50)",
)
@click.option(
    "--offset",
    default=0,
    required=False,
    help="Starting position for pagination (default: 0)",
)
@click.option(
    "--filter",
    required=False,
    multiple=True,
    help="Filter nodes by conditions (e.g., 'status=fail', 'name=test_*'). Can be used multiple times",
)
@click.option(
    "--field",
    required=False,
    multiple=True,
    help="Display only specific field(s) from node data (e.g., 'name', 'status'). Can be used multiple times",
)
@click.pass_context
def maestro_results(ctx, nodeid, nodes, limit, offset, filter, field):
    config = ctx.obj.get("CFG")
    instance = ctx.obj.get("INSTANCE")
    url = config[instance]["api"]
    if not nodeid and not nodes:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        sys.exit(0)
    if nodeid:
        results = maestro_get_node(url, nodeid)
    if nodes:
        results = maestro_get_nodes(url, limit, offset, filter)
    maestro_print_nodes(results, field)


if __name__ == "__main__":
    main_kcidev()
