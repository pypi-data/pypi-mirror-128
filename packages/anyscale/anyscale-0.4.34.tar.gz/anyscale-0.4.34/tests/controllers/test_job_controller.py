import json
from typing import Optional
from unittest.mock import Mock, mock_open, patch

import pytest

from anyscale.client.openapi_client import CreateProductionJob, ProductionJobConfig
from anyscale.controllers.job_controller import JobController


def test_submit_job(
    base_mock_api_client: Mock, base_mock_anyscale_api_client: Mock,
) -> None:
    job_controller = JobController(
        api_client=base_mock_api_client,
        anyscale_api_client=base_mock_anyscale_api_client,
    )
    mock_project_definition = Mock()
    mock_project_definition.root = "/some/directory"
    mock_load_project_or_throw = Mock(return_value=mock_project_definition)

    mock_get_project_id = Mock(return_value="mock_project_id")

    mock_config_dict = {
        "entrypoint": "mock_entrypoint",
        "build_id": "mock_build_id",
        "compute_config_id": "mock_compute_config_id",
    }
    with patch(
        "builtins.open", mock_open(read_data=json.dumps(mock_config_dict))
    ), patch.multiple(
        "anyscale.controllers.job_controller",
        load_project_or_throw=mock_load_project_or_throw,
        get_project_id=mock_get_project_id,
    ), patch.multiple(
        "os.path", exists=Mock(return_value=True)
    ):
        job_controller.submit(
            "mock_config_file", name="mock_name", description="mock_description"
        )

    job_controller.api_client.create_job_api_v2_decorated_ha_jobs_create_post.assert_called_once_with(
        CreateProductionJob(
            name="mock_name",
            description="mock_description",
            project_id="mock_project_id",
            config=ProductionJobConfig(**mock_config_dict),
        )
    )


@pytest.mark.parametrize("include_all_users", [False, True])
@pytest.mark.parametrize("name", ["mock_job_name", None])
@pytest.mark.parametrize("job_id", ["mock_job_id", None])
@pytest.mark.parametrize("project_id", ["mock_project_id", None])
def test_list_jobs(
    base_mock_api_client: Mock,
    base_mock_anyscale_api_client: Mock,
    include_all_users: bool,
    name: Optional[str],
    job_id: Optional[str],
    project_id: Optional[str],
) -> None:
    job_controller = JobController(
        api_client=base_mock_api_client,
        anyscale_api_client=base_mock_anyscale_api_client,
    )
    job_controller.api_client.get_user_info_api_v2_userinfo_get = Mock(
        return_value=Mock(result=Mock(id="mock_user_id"))
    )
    job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get = Mock(
        return_value=Mock(results=[Mock(config=Mock(entrypoint=""))])
    )
    job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get = Mock(
        return_value=Mock(result=Mock(config=Mock(entrypoint="")))
    )

    job_controller.list(
        include_all_users=include_all_users,
        name=name,
        job_id=job_id,
        project_id=project_id,
    )

    if job_id:
        job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get.assert_called_once_with(
            job_id
        )
        job_controller.api_client.get_user_info_api_v2_userinfo_get.assert_not_called()
        job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.assert_not_called()
    else:
        creator_id: Optional[str] = None
        if not include_all_users:
            creator_id = "mock_user_id"
            job_controller.api_client.get_user_info_api_v2_userinfo_get.assert_called_once()
        else:
            job_controller.api_client.get_user_info_api_v2_userinfo_get.assert_not_called()
        job_controller.api_client.get_job_api_v2_decorated_ha_jobs_production_job_id_get.assert_not_called()
        job_controller.api_client.list_decorated_jobs_api_v2_decorated_ha_jobs_get.assert_called_once_with(
            creator_id=creator_id, name=name, project_id=project_id
        )


def test_terminate_job(
    base_mock_api_client: Mock, base_mock_anyscale_api_client: Mock,
) -> None:
    job_controller = JobController(
        api_client=base_mock_api_client,
        anyscale_api_client=base_mock_anyscale_api_client,
    )
    job_controller.terminate("mock_job_id")

    job_controller.api_client.terminate_job_api_v2_decorated_ha_jobs_production_job_id_terminate_post.assert_called_once_with(
        "mock_job_id"
    )
