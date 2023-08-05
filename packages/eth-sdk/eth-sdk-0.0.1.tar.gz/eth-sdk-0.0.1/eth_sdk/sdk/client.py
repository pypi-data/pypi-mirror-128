from eth_sdk.abi_management import networks, fetch_abis
from eth_sdk.config import read_config, ConfigurationError
from web3 import Web3
import os
import dotsi
import logging

logging.basicConfig(level=logging.INFO)


class EthSdk:
	def __init__(self, network, signer):
		self.root_path = os.path.abspath(os.curdir)
		self.config = read_config(self.root_path, network)
		self.addresses = dotsi.Dict(self.config['contracts'])

		if 'rpc' in self.config:
			self.rpc = self.config['rpc']
		else:
			self.rpc = networks.get_rpc_provider(network)
			logging.warn(f"An RPC provider wasn't included in config.yml. Falling back to the default for {network}")

		if 'etherscan' in self.config:
			try:
				self.api_url = self.config['etherscan']['url']
				self.api_key = self.config['etherscan']['api_key']
			except KeyError:
				raise ConfigurationError("You should include both `url` and `api_key` under etherscan")
		else:
			self.api_url = networks.get_api_url(network)
			self.api_key = networks.get_api_key(network)
			logging.warn(f"Etherscan info wasn't included in config.yml. Falling back to the default for {network}")

		self.contract_abis = fetch_abis(self.root_path, network, self.addresses, self.api_key)
		self.w3 = Web3(Web3.HTTPProvider(self.rpc))
		self.w3.eth.default_account = signer
		self.contracts = self.build_contracts()


	def build_contracts(self):
		contracts_sdk = {}
		for contract in self.config['contracts']:
			abi = self.contract_abis[contract]
			address = self.addresses[contract]
			contracts_sdk[contract] = self.w3.eth.contract(address=address, abi=abi)

		return dotsi.Dict(contracts_sdk)


	def build_contracts_sdk(self):
		contracts_sdk = {}
		for contract in self.config['contracts']:
			abi = self.contract_abis[contract]
			address = self.addresses[contract]
			contracts_sdk[contract] = self.w3.eth.contract(address=address, abi=abi).caller

		return dotsi.Dict(contracts_sdk)


def eth_sdk(network, signer):
	sdk = EthSdk(network, signer)
	
	return sdk.build_contracts_sdk()

