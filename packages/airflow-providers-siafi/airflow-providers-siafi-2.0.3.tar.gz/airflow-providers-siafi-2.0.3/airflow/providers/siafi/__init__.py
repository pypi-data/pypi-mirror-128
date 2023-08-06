__all__ = ['VERSION']

import yaml
import os

VERSION = '2.0.3'


def get_provider_info() -> dict:
    '''Retorna metadados do provider.'''

    base_dirpath = os.path.abspath(os.path.dirname(__file__))

    with open(os.path.join(base_dirpath, 'provider.yaml'), 'rt') as fd:
        return yaml.safe_load(fd)
