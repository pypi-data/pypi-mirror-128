from unittest.mock import patch

import pytest

from sym.flow.cli.errors import SymAPIError
from sym.flow.cli.models.service import Service
from sym.flow.cli.models.service_type import MANAGED_SERVICES, ServiceType
from sym.flow.cli.symflow import symflow as click_command


class TestServicesDelete:
    MOCK_SLACK_SERVICE = Service(
        id="fake-uuid", slug="slack", external_id="T123ABC", label="Slack"
    )

    @patch("sym.flow.cli.helpers.api.SymAPI.get_service", return_value=MOCK_SLACK_SERVICE)
    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_service_references",
        return_value={"identities": [], "integrations": []},
    )
    @patch("sym.flow.cli.helpers.api.SymAPI.delete_service")
    @patch("sym.flow.cli.commands.services.services_delete.pre_service_delete_hooks")
    def test_services_delete(
        self,
        mock_pre_delete_hooks,
        mock_delete_service,
        mock_get_service_references,
        mock_get_service,
        click_setup,
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                [
                    "services",
                    "delete",
                    "--service-type",
                    self.MOCK_SLACK_SERVICE.service_type,
                    "--external-id",
                    self.MOCK_SLACK_SERVICE.external_id,
                ],
            )
            assert result.exit_code == 0
            assert (
                f"Successfully deleted service type slack with external ID {self.MOCK_SLACK_SERVICE.external_id}!"
                in result.output
            )
            mock_pre_delete_hooks.assert_called_once()
            mock_pre_delete_hooks.call_args.args[1] == self.MOCK_SLACK_SERVICE
            mock_get_service.assert_called_once()
            mock_delete_service.assert_called_once()

    @pytest.mark.parametrize(
        "service_type",
        [s.value for s in ServiceType if s.type_name not in MANAGED_SERVICES],
    )
    def test_services_delete_prompt_external_id(self, service_type, click_setup):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                ["services", "delete", "--service-type", service_type.type_name],
                input="^C",
            )
            # Check that the printed external ID is the one associated with the given service_type
            assert service_type.external_id_name in result.output

    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_service",
        side_effect=SymAPIError,
    )
    @patch("sym.flow.cli.helpers.api.SymAPI.delete_service")
    def test_services_delete_not_found_errors(
        self, mock_delete_service, mock_get_service, click_setup
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                [
                    "services",
                    "delete",
                    "--service-type",
                    "slack",
                    "--external-id",
                    "T123ABC",
                ],
            )
            mock_get_service.assert_called_once()
            mock_delete_service.assert_not_called()
            assert result.exit_code is not 0

    @patch("sym.flow.cli.helpers.api.SymAPI.get_service", return_value=MOCK_SLACK_SERVICE)
    @patch(
        "sym.flow.cli.helpers.api.SymAPI.get_service_references",
        return_value={"identities": ["uuid1"], "integrations": ["uuid2"]},
    )
    @patch("sym.flow.cli.helpers.api.SymAPI.delete_service")
    @patch("sym.flow.cli.commands.services.services_delete.pre_service_delete_hooks")
    def test_services_delete_has_references(
        self,
        mock_pre_delete_hooks,
        mock_delete_service,
        mock_get_service_references,
        mock_get_service,
        click_setup,
    ):
        with click_setup() as runner:
            result = runner.invoke(
                click_command,
                [
                    "services",
                    "delete",
                    "--service-type",
                    self.MOCK_SLACK_SERVICE.service_type,
                    "--external-id",
                    self.MOCK_SLACK_SERVICE.external_id,
                ],
            )
            mock_get_service.assert_called_once()
            mock_get_service_references.assert_called_once()
            mock_pre_delete_hooks.assert_not_called()
            mock_delete_service.assert_not_called()
            assert result.exit_code is not 0
            assert (
                f"Cannot perform delete because it is referenced by 1 identities and 1 integrations"
                in result.output
            )
