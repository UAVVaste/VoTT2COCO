import json
import yaml
import click

from utils import VOTTReader, COCOSaver


def parse_config_file(config_file) -> dict:
    """Read config.yaml file with params.
    Returns
    -------
    dict
        Dict of config
    """
    with open(config_file, 'r') as stream:
        try:
            CONFIG = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    return CONFIG

@click.command()
@click.option('--config', '-c', required=True, help='Config path')
def main(config):
    CONFIG = parse_config_file(config)

    reader = VOTTReader(CONFIG)
    reader.parse_files()

    saver = COCOSaver(CONFIG, reader)
    saver.save()

if __name__ == "__main__":
    main()
