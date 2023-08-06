import pytest

from jelastic_client import ControlClient, JpsClient
from jelastic_client.core.exceptions import JelasticClientException
from test_utils.manifest_data import get_manifest_data


def test_jps_client_install_from_file_valid_manifest_file_creates_environment(
        control_client: ControlClient,
        jps_client: JpsClient,
        valid_manifest_file,
        new_env_name: str):
    # Arrange

    # Act
    jps_client.install_from_file(valid_manifest_file, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.exists()


def test_jps_client_install_from_url_valid_manifest_url_creates_environment(
        control_client: ControlClient,
        jps_client: JpsClient,
        valid_manifest_url: str,
        new_env_name: str):
    # Arrange

    # Act
    jps_client.install_from_url(valid_manifest_url, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.exists()


def test_jps_client_install_from_file_valid_manifest_file_makes_environment_run(
        control_client: ControlClient,
        jps_client: JpsClient,
        valid_manifest_file,
        new_env_name: str):
    # Arrange

    # Act
    jps_client.install_from_file(valid_manifest_file, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.is_running()


def test_jps_client_install_from_url_valid_manifest_url_makes_environment_run(
        control_client: ControlClient,
        jps_client: JpsClient,
        valid_manifest_url,
        new_env_name: str):
    # Arrange

    # Act
    jps_client.install_from_url(valid_manifest_url, new_env_name)

    # Assert
    env_info = control_client.get_env_info(new_env_name)
    assert env_info.is_running()


def test_jps_client_install_from_file_valid_manifest_file_returns_success_text(
        jps_client: JpsClient,
        valid_manifest_file,
        new_env_name: str):
    # Arrange

    # Act
    actual_success_text = jps_client.install_from_file(
        valid_manifest_file, new_env_name)

    # Assert
    expected_success_text = "<strong>Field1</strong>: Value1<br />\n<strong>Field2</strong>: Value2"
    assert expected_success_text == actual_success_text


def test_jps_client_install_from_url_valid_manifest_url_returns_success_text(
        jps_client: JpsClient,
        valid_manifest_url,
        new_env_name: str):
    # Arrange

    # Act
    actual_success_text = jps_client.install_from_url(
        valid_manifest_url, new_env_name)

    # Assert
    expected_success_text = "<strong>Field1</strong>: Value1<br />\n<strong>Field2</strong>: Value2"
    assert expected_success_text == actual_success_text


def test_jps_client_install_from_file_invalid_manifest_file_raises_exception(
        jps_client: JpsClient,
        invalid_manifest_file,
        new_env_name: str):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_file(invalid_manifest_file, new_env_name)


def test_jps_client_install_from_url_invalid_manifest_url_raises_exception(
        jps_client: JpsClient,
        invalid_manifest_url: str,
        new_env_name: str):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_url(invalid_manifest_url, new_env_name)


def test_jps_client_install_from_file_non_existent_manifest_file_raises_exception(
        jps_client: JpsClient,
        non_existent_manifest_file,
        new_env_name: str):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_file(non_existent_manifest_file, new_env_name)


def test_jps_client_install_from_url_non_existent_manifest_url_raises_exception(
        jps_client: JpsClient,
        non_existent_manifest_url,
        new_env_name: str):
    # Arrange

    # Act / Assert
    with pytest.raises(JelasticClientException):
        jps_client.install_from_url(non_existent_manifest_url, new_env_name)


def test_jps_client_install_from_file_manifest_file_with_settings_takes_settings_into_account(
        jps_client: JpsClient,
        manifest_file_with_settings):
    # Arrange
    expected_settings = {
        "field1": "the value 1",
        "field2": "the value 2"
    }

    # Act
    success_text = jps_client.install_from_file(
        manifest_file_with_settings,
        settings=expected_settings)
    manifest_data = get_manifest_data(success_text)

    # Assert
    for field in expected_settings:
        assert field in manifest_data
        assert expected_settings[field] == manifest_data[field]


def test_jps_client_install_from_url_manifest_url_with_settings_takes_settings_into_account(
        jps_client: JpsClient,
        manifest_url_with_settings):
    # Arrange
    expected_settings = {
        "field1": "the value 1",
        "field2": "the value 2"
    }

    # Act
    success_text = jps_client.install_from_url(
        manifest_url_with_settings,
        settings=expected_settings)
    manifest_data = get_manifest_data(success_text)

    # Assert
    for field in expected_settings:
        assert field in manifest_data
        assert expected_settings[field] == manifest_data[field]


def test_jps_client_get_engine_version_returns_supported_engine_version(
        jps_client: JpsClient,
        supported_jelastic_version: str):
    # Arrange

    # Act
    actual_version = jps_client.get_engine_version()

    # Assert
    assert supported_jelastic_version == actual_version
