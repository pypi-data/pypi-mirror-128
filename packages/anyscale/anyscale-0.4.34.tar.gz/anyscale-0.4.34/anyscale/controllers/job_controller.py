from datetime import datetime
import os
from typing import Optional

import click
import tabulate
import yaml

from anyscale.api import get_anyscale_api_client, get_api_client
from anyscale.cli_logger import _CliLogger
from anyscale.client.openapi_client import CreateProductionJob, ProductionJobConfig
from anyscale.client.openapi_client.api.default_api import DefaultApi
from anyscale.project import get_project_id, load_project_or_throw


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
        try:
            config_object = ProductionJobConfig(**config_dict)
        except TypeError as e:
            # TODO(nikita): Include more details in error message on what the correct format should be.
            raise click.ClickException(
                f"{e}\n{job_config_file} is not in the correct format for a ProductionJobConfig."
            )

        job = self.api_client.create_job_api_v2_decorated_ha_jobs_create_post(
            CreateProductionJob(
                name=name or "cli-job-{}".format(datetime.now().isoformat()),
                description=description or "Job submitted from CLI",
                project_id=project_id,
                config=config_object,
            )
        ).result

        self.log.info(
            f"Job {job.id} has been successfully submitted. Current state of job: {job.state.current_state}."
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

        jobs_table = []
        for job in jobs_list:
            jobs_table.append(
                [
                    job.name,
                    job.id,
                    job.cost_dollars,
                    job.project.name,
                    job.state.cluster.name,
                    job.state.current_state,
                    job.creator.username,
                    job.config.entrypoint
                    if len(job.config.entrypoint) < 50
                    else job.config.entrypoint[:50] + " ...",
                ]
            )
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
