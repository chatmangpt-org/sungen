import pytest
from pathlib import Path
from sungen.utils.plugin_tools import (
    PluginSettings,
    DependencyConfig,
    CompatibilityConfig,
    MarketplaceConfig,
    SupportConfig,
    AdvancedOptionsConfig,
    create_plugin_yaml,
    load_plugin_config,
    get_plugin_metadata,
    validate_plugin_compatibility,
)


# Define a temporary directory for testing
@pytest.fixture(scope="module")
def temp_dir(tmpdir_factory):
    return tmpdir_factory.mktemp("test_plugins")


@pytest.fixture

def sample_plugin_config():
    """Fixture to provide a sample plugin configuration for testing."""
    return PluginSettings(
        name="Marketplace Plugin",
        short_name="mrkt",
        version="1.0.0",
        description="The Marketplace Plugin enables seamless integration with the Sungen marketplace.",
        author="Sungen Team",
        source="https://github.com/sungen/mrkt-plugin",
        license="MIT",
        tags=["marketplace", "plugin-management", "sungen"],
        settings={
            "default_marketplace": "https://marketplace.sungen.com",
            "cache_timeout": 300,
            "auto_update_check": True,
            "log_level": "INFO",
            "retry_count": 3,
            "connection_timeout": 30,
            "backup_before_update": True,
        },
        dependencies=[
            DependencyConfig(plugin="core-plugin", version=">=1.0.0"),
            DependencyConfig(plugin="auth-plugin", version=">=1.0.0")
        ],
        compatibility=CompatibilityConfig(
            min_sungen_version="1.0.0",
            max_sungen_version="2.0.0"
        ),
        marketplace=MarketplaceConfig(
            featured=True,
            category="Utilities",
            keywords=["plugin", "marketplace", "utilities"]
        ),
        support=SupportConfig(
            documentation_url="https://docs.sungen.com/mrkt-plugin",
            issues_url="https://github.com/sungen/mrkt-plugin/issues",
            contact_email="support@sungen.com"
        ),
        advanced=AdvancedOptionsConfig(
            parallel_install=True,
            secure_downloads=True,
            sandbox_mode=False
        )
    )


def test_create_plugin_yaml(sample_plugin_config, tmp_path):
    """Test creating a plugin YAML configuration file."""
    file_path = tmp_path / "plugin.yaml"
    create_plugin_yaml(sample_plugin_config, str(file_path))

    assert file_path.exists(), "YAML file should be created."
    with open(file_path) as f:
        assert "name: Marketplace Plugin" in f.read(), "YAML should contain the plugin name."


def test_load_plugin_config(sample_plugin_config, tmp_path):
    """Test loading a plugin configuration from YAML file."""
    file_path = tmp_path / "plugin.yaml"
    create_plugin_yaml(sample_plugin_config, str(file_path))

    loaded_config = load_plugin_config(str(file_path))
    assert loaded_config.name == "Marketplace Plugin", "Loaded configuration should match."


def test_get_plugin_metadata(sample_plugin_config):
    """Test retrieving metadata from plugin configuration."""
    metadata = get_plugin_metadata(sample_plugin_config)
    assert metadata["name"] == "Marketplace Plugin"
    assert metadata["short_name"] == "mrkt"
    assert metadata["version"] == "1.0.0"


def test_validate_plugin_compatibility(sample_plugin_config):
    """Test validating plugin compatibility with the Sungen version."""
    assert validate_plugin_compatibility(sample_plugin_config, "1.5.0"), "Plugin should be compatible."
    assert not validate_plugin_compatibility(sample_plugin_config, "2.5.0"), "Plugin should not be compatible."


def test_validate_plugin_compatibility_edge_case(sample_plugin_config):
    """Test compatibility at the edges of the supported version range."""
    assert validate_plugin_compatibility(sample_plugin_config,
                                         "1.0.0"), "Plugin should be compatible at minimum version."
    assert validate_plugin_compatibility(sample_plugin_config,
                                         "2.0.0"), "Plugin should be compatible at maximum version."
    assert not validate_plugin_compatibility(sample_plugin_config,
                                             "0.9.9"), "Plugin should not be compatible below minimum version."
    assert not validate_plugin_compatibility(sample_plugin_config,
                                             "2.0.1"), "Plugin should not be compatible above maximum version."


def test_create_plugin_yaml_creates_directory_if_not_exists(sample_plugin_config, tmp_path):
    """Test that create_plugin_yaml creates directory if it does not exist."""
    non_existent_dir = tmp_path / "non_existent_dir"
    file_path = non_existent_dir / "plugin.yaml"

    create_plugin_yaml(sample_plugin_config, str(file_path))

    assert file_path.exists(), "YAML file should be created even if directory does not exist."
