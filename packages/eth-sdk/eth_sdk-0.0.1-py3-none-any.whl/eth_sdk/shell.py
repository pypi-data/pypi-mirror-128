import click
import yaml
import os


CONFIG_TEMPLATE = {
	'mainnet': {
		'contracts':  {
			'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
		},
		'rpc':'https://mainnet.infura.io/v3/4210ba8eb536423e8ae5d774c5064fa1',
		'etherscan': {
			'url': 'https://api.etherscan.io/api',
			'api_key': 'ICZKZRP33RIZSYZJSJJ1S1ZNU64CY3KDNG'
		},
	}
}


def cli():
	create_eth_dir()

	with open("./eth-sdk/config.yml", "w") as f:
		yaml.dump(CONFIG_TEMPLATE, f)

	click.echo("Created config.yml file")
	click.echo("eth-sdk will automatically fetch the ABI from etherscan from validated contracts in this file")


def create_eth_dir():
	try:
		os.mkdir("eth-sdk")
	except FileExistsError:
		pass