from kernel.core import Core

from .config import configs
from .events import *


def create_core(env: str) -> Core:
    from .controllers import controllers

    if env not in configs:
        raise ValueError('invalid environment')

    core = Core(import_name=__name__, config=configs[env].to_dict())

    return core
