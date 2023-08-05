import requests
import json
from eth_sdk.abi_management.networks import get_api_url
from eth_sdk.system.utils import resolve_path_from_base, path_exists, create_dir, join_paths
from eth_sdk.system import SDK_PATHS


class AbiRequestError(Exception):
    pass

class InvalidApiKey(Exception):
    pass

class InvalidAddress(Exception):
    pass



def get_abi(network_name: str, contract_address: str, api_key: str) -> dict:
	api_url = get_api_url(network_name)

	url = (
	    f"{api_url}?module=contract"
		"&action=getabi"
		f"&address={contract_address}"
		f"&apikey={api_key}"
	)

	r = requests.get(url)
	
	try:
		result = r.json()['result']
	except TypeError:
		raise AbiRequestError(f"Request to {url} was unsuccessful")

	if result == 'Invalid API Key':
		raise InvalidApiKey("The provided API is not valid")

	if result == 'Invalid Address format':
		raise InvalidAddress(f"Address {contract_address} in config.yml is invalid")

	return json.loads(result)


def fetch_abis(project_root: str, network: str, contracts: dict, api_key: str) -> dict:
	contract_abis = {}
	for path in SDK_PATHS:
		sdk_path = resolve_path_from_base(
			path, project_root
		)
		if path_exists(sdk_path):
			abi_folder = join_paths(sdk_path, 'abi')
			network_folder = join_paths(abi_folder, network)

			if not path_exists(abi_folder):
				print("No ABI folder exists creating a new one")
				create_dir(abi_folder)

			if not path_exists(network_folder):
				print(f"No abi/{network} folder exists creating a new one")
				create_dir(network_folder)

			for contract in contracts:
				contract_address = contracts[contract]
				contract_abi_file = join_paths(network_folder, f"{contract}.json")

				if not path_exists(contract_abi_file):
					abi_json = get_abi(network, contract_address, api_key)
					write_json(contract_abi_file, abi_json)
				else:
					with open(contract_abi_file, "r") as f:
						abi_json = json.load(f)

				contract_abis[contract] = abi_json

			return contract_abis


def write_json(filename: str, payload: dict) -> None:
	with open(filename, 'w') as f:
		json.dump(payload, f, indent=4)