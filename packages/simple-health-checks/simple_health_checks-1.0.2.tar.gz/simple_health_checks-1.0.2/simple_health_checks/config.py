import os
from importlib import import_module
from pathlib import Path

from dynaconf import (
    Dynaconf,
    Validator,
)

settings = Dynaconf(
    envvar_prefix="HEALTH_CHECKS",
    validators=[
        Validator("RESOURCES", default=[]),
        Validator("CRITICAL", default=[]),
        Validator("SERVICE_NAME", default=""),
        Validator("CACHE_SECONDS", cast=int, default=5),
        Validator("TIMEOUT", cast=int, default=10),
        Validator("MAX_WORKERS", cast=int, default=2),
        Validator("SERVICE_VERSION", default=""),
    ],
)

# pylint: disable=invalid-name
config_path = f"{Path(os.path.dirname(os.path.realpath(__file__)))}/additional_configs/"
config_packages = "simple_health_checks.additional_configs.{}"
filenames = []
if os.path.isdir(config_path):
    filenames = [
        filename for filename in os.listdir(config_path) if "config" in filename
    ]

for filename in filenames:
    validators = import_module(config_packages.format(filename[:-3])).validators
    settings.validators.register(*validators)

settings.validators.validate()
