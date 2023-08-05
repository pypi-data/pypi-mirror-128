from datetime import datetime
import os
from typing import Any, Optional

import click
from pydantic import BaseModel, Field, root_validator
import tabulate
import yaml

from anyscale.api import get_anyscale_api_client, get_api_client
from anyscale.cli_logger import _CliLogger
from anyscale.client.openapi_client import CreateProductionJob, ProductionJobConfig
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.cluster_compute import (
    get_cluster_compute_id_from_name,
    get_default_cluster_compute_id,
)
from anyscale.cluster_env import get_build_id_from_cluster_env_identifier
from anyscale.project import get_project_id, load_project_or_throw


class JobConfig(BaseModel):
    """
    Synchronize with ray.dashboard.modules.job.sdk.ClusterInfo
    """

    entrypoint: str = Field(
        ...,
        description="A script that will be run to start your job. This command will be run in the root directory of the specified runtime env. Eg. 'python script.py'",
    )
    name: Optional[str] = Field(
        None,
        description="Name of job to be submitted. Default will be used if not provided.",
    )
    description: Optional[str] = Field(
        None,
        description="Description of job to be submitted. Default will be used if not provided.",
    )
    runtime_env: Optional[Any] = Field(
        None,
        description="A ray runtime env json. Your entrypoint will be run in the environment specified by this runtime env.",
    )
    build_id: Optional[str] = Field(
        None,
        description="The id of the cluster env build. This id will determine the docker image your job is run on.",
    )
    cluster_env: Optional[str] = Field(
        None,
        description="The name of the cluster environment and build revision in format `my_cluster_env:1`.",
    )
    compute_config_id: Optional[str] = Field(
        None,
        description="The id of the compute configuration that you want to use. This id will specify the resources required for your job",
    )
    compute_config: Optional[str] = Field(
        None,
        description="The name of the compute configuration that you want to use. This will specify the resources required for your job",
    )
    cloud: Optional[str] = Field(
        None,
        description="The cloud name to specify a default compute configuration with. This will specify the resources required for your job",
    )
    max_retries: Optional[int] = Field(
        5,
        description="The number of retries this job will attempt on failure. Set to None to set infinite retries",
    )

    @root_validator
    def fill_build_id(cls: Any, values: Any) -> Any:  # noqa: N805
        build_id, cluster_env = (
            values.get("build_id"),
            values.get("cluster_env"),
        )
        if not cluster_env and not build_id:
            raise click.ClickException(
                "Either `cluster_env` or `build_id` must be provided in the job config file."
            )
        if cluster_env and build_id:
            raise click.ClickException(
                "Both `cluster_env` or `build_id` cannot be provided in the job config file. "
                "Please only provided one of these fields."
            )
        if cluster_env:
            build_id = get_build_id_from_cluster_env_identifier(cluster_env)
            values["build_id"] = build_id
        return values

    @root_validator
    def fill_compute_config_id(cls: Any, values: Any) -> Any:  # noqa: N805
        compute_config_id, compute_config, cloud = (
            values.get("compute_config_id"),
            values.get("compute_config"),
            values.get("cloud"),
        )
        if not compute_config_id and not compute_config and not cloud:
            raise click.ClickException(
                "Either `compute_config_id` or `compute_config` or `cloud` must be provided in the job config file."
            )
        if (bool(compute_config_id) + bool(compute_config) + bool(cloud)) > 1:
            raise click.ClickException(
                "Please only provided one of `compute_config_id` or `compute_config` or `cloud` in the "
                "job config file."
            )
        if compute_config:
            compute_config_id = get_cluster_compute_id_from_name(compute_config)
            values["compute_config_id"] = compute_config_id
        elif cloud:
            compute_config_id = get_default_cluster_compute_id(cloud)
            values["compute_config_id"] = compute_config_id

        return values


class JobController:
    def __init__(
        self,
        api_client: Optional[DefaultApi] = None,
        anyscale_api_client: Optional[DefaultApi] = None,
        log: _CliLogger = _CliLogger(),
    ):
        if api_client is None:
            api_client = get_api_client()
        if anyscale_api_client is None:
            anyscale_api_client = get_anyscale_api_client()
        self.api_client = api_client
        self.anyscale_api_client = anyscale_api_client
        self.log = log

    def submit(
        self, job_config_file: str, name: Optional[str], description: Optional[str]
    ) -> None:
        # TODO(nikita): Remove dependency on project context by providing project_id arg and supporting
        # default projects.
        project_definition = load_project_or_throw()
        project_id = get_project_id(project_definition.root)

        if not os.path.exists(job_config_file):
            raise click.ClickException(f"Config file {job_config_file} not found")

        with open(job_config_file, "r") as f:
            config_dict = yaml.safe_load(f)

        job_config = JobConfig.parse_obj(config_dict)
        config_object = ProductionJobConfig(
            entrypoint=job_config.entrypoint,
            runtime_env_config=job_config.runtime_env,
            build_id=job_config.build_id,
            compute_config_id=job_config.compute_config_id,
            max_retries=job_config.max_retries,
        )

        job = self.api_client.create_job_api_v2_decorated_ha_jobs_create_post(
            CreateProductionJob(
                name=name
                or job_config.name
                or "cli-job-{}".format(datetime.now().isoformat()),
                description=description
                or job_config.description
                or "Job submitted from CLI",
                project_id=project_id,
                config=config_object,
            )
        ).result

        self.log.info(
            f"Job {job.id} has been successfully submitted. Current state of job: {job.state.current_state}."
        )
        self.log.info(
            f"Query the status of the job with `anyscale job list --job-id {job.id}`."
        )

    def list(
        self,
        include_all_users: bool,
        name: Optional[str],
        job_id: Optional[str],
        project_id: Optional[str],
    ) -> None:
        jobs_list = []
        if job_id:
            job = self.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get(
                job_id
            ).result
            jobs_list.append(job)
        else:
            if not include_all_users:
                creator_id = (
                    self.api_client.get_user_info_api_v2_userinfo_get().result.id
                )
            else:
                creator_id = None
            jobs_resp = self.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get(
                project_id=project_id, name=name, creator_id=creator_id
            ).results
            jobs_list.extend(jobs_resp)

        jobs_table = [
            [
                job.name,
                job.id,
                job.cost_dollars,
                job.project.name,
                job.state.cluster.name if job.state.cluster else None,
                job.state.current_state,
                job.creator.username,
                job.config.entrypoint
                if len(job.config.entrypoint) < 50
                else job.config.entrypoint[:50] + " ...",
            ]
            for job in jobs_list
        ]

        table = tabulate.tabulate(
            jobs_table,
            headers=[
                "NAME",
                "ID",
                "COST",
                "PROJECT NAME",
                "CLUSTER NAME",
                "CURRENT STATE",
                "CREATOR",
                "ENTRYPOINT",
            ],
            tablefmt="plain",
        )
        print(f"Jobs:\n{table}")

    def terminate(self, job_id: str,) -> None:
        job = self.api_client.terminate_job_api_v2_decorated_ha_jobs_production_job_id_terminate_post(
            job_id
        ).result

        self.log.info(f"Job {job.id} has begun terminating...")
        self.log.info(
            f" Current state of job: {job.state.current_state}. Goal state of job: {job.state.goal_state}"
        )
        self.log.info(
            f"Query the status of the job with `anyscale job list --job-id {job.id}`."
        )
