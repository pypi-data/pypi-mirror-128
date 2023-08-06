from pathlib import Path

import yaml


CONFIG_PATH = Path('.phantom-dev.yaml')


def load_config(path: Path = CONFIG_PATH):
	with path.open() as config_file:
		return yaml.safe_load(config_file)
