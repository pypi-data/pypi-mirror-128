import os
import yaml

from eth_sdk.system.utils import resolve_path_from_base, path_exists
from eth_sdk.system import SDK_PATHS


class ConfigurationError(Exception):
    pass

class ConfigurationNotFound(Exception):
	pass


def read_config(project_root: str, network: str) -> dict:
	config_dict = None
	for path in SDK_PATHS:
		filename = path + 'config.yml'
		config_filepath = resolve_path_from_base(
			filename, project_root
		)

		if path_exists(config_filepath):
			config_missing = False
			config_dict = _load_yaml(config_filepath)
			try:
				network_config = config_dict[network]
			except KeyError:
				raise ConfigurationError(f"Network {network} wan't found in your config.yml file")
			break

		else:
			config_missing = True

	if config_missing:
		raise ConfigurationNotFound("A config.yml file wasn't found. Include one inside the eth-sdk folder or run eth-sdk --init on the root folder")
	
	return network_config


def _load_yaml(config_filepath: str) -> dict:
	with open(config_filepath, 'r') as f:
		config = yaml.safe_load(f)
		
	return config