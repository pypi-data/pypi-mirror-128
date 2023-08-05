import click
import yaml
import os


CONFIG_TEMPLATE = {
	'mainnet': {
		'contracts':  {
			'dai': '0x6B175474E89094C44Da98b954EedeAC495271d0F',
			'usdc': '0x00000'
		},
		'rpc':'https://mainnet.infura.io/v3/00000000000000000000000000000000',
		'etherscan': {
			'url': 'https://api.etherscan.io/api',
			'api_key': 'YOUR_KEY'
		},
	}
}


@click.command()
@click.option('--init', required=True, is_flag=True, help='Initialize eth-sdk project')
def cli(init):
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