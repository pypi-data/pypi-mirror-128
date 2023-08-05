from typing import List, Optional

import click

from anyscale.api import get_anyscale_api_client
from anyscale.cli_logger import _CliLogger
from anyscale.client.openapi_client import Build
from anyscale.client.openapi_client.api.default_api import DefaultApi


log = _CliLogger()


def get_build_id_from_cluster_env_identifier(
    cluster_env_identifier: str, anyscale_api_client: Optional[DefaultApi] = None,
) -> str:
    """
    Get a build id from a cluster environment identifier of form `my_cluster_env:1` or
    `my_cluster_env`. If no build revision is specified, return id of latest build
    for this application config.

    TODO(nikita): Move this to behind api endpoint and consolidate with anyscale.connect
    """

    if anyscale_api_client is None:
        anyscale_api_client = get_anyscale_api_client()
    try:
        components = cluster_env_identifier.rsplit(":", 1)
        cluster_env_name = components[0]
        cluster_env_revision = int(components[1]) if len(components) > 1 else None
    except ValueError:
        raise click.ClickException(
            "Invalid cluster-env-name provided. Please make sure the provided name is of "
            "the form <cluster-env-name>:<revision>. For example, `my_cluster_env:1`."
        )

    # ID of cluster env and not build itself
    cluster_env_id = get_cluster_env_id_from_name(cluster_env_name, anyscale_api_client)

    builds = list_builds(cluster_env_id, anyscale_api_client)
    if cluster_env_revision:
        for build in builds:
            if build.revision == cluster_env_revision:
                return str(build.id)

        raise click.ClickException(
            "Revision {} of cluster environment '{}' not found.".format(
                cluster_env_revision, cluster_env_name
            )
        )
    else:
        latest_build_revision = -1
        build_to_use = None
        for build in builds:
            if build.revision > latest_build_revision:
                latest_build_revision = build.revision
                build_to_use = build

        if not build_to_use:
            raise click.ClickException(
                "Error finding latest build of cluster environment {}. Please manually "
                "specify the build version in the cluster environment name with the format "
                "<cluster-env-name>:<revision>. For example, `my_cluster_env:1`.".format(
                    cluster_env_name
                )
            )
        return str(build_to_use.id)


def get_cluster_env_id_from_name(
    cluster_env_name: str, anyscale_api_client: Optional[DefaultApi] = None,
) -> str:
    """
    Get id of the cluster env (not build) given the name.
    """

    if anyscale_api_client is None:
        anyscale_api_client = get_anyscale_api_client()
    cluster_envs = anyscale_api_client.search_cluster_environments(
        {"name": {"equals": cluster_env_name}, "paging": {"count": 1}}
    ).results
    for cluster_env in cluster_envs:
        if cluster_env.name == cluster_env_name:
            return str(cluster_env.id)

    raise click.ClickException(
        "Cluster environment '{}' not found. ".format(cluster_env_name)
    )


def list_builds(
    cluster_env_id: str, anyscale_api_client: Optional[DefaultApi] = None,
) -> List[Build]:
    """
    List all builds for a given cluster env id.
    """

    if anyscale_api_client is None:
        anyscale_api_client = get_anyscale_api_client()
    entities = []
    has_more = True
    while has_more:
        resp = anyscale_api_client.list_cluster_environment_builds(
            cluster_env_id, count=50, paging_token=None
        )
        entities.extend(resp.results)
        paging_token = resp.metadata.next_paging_token
        has_more = paging_token is not None
    return entities
