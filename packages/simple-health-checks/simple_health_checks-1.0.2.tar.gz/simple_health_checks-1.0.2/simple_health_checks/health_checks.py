import concurrent.futures
import logging
from datetime import datetime
from importlib import import_module
from time import time

from pebble import ProcessPool

import simple_health_checks
from simple_health_checks.config import settings
from simple_health_checks.enums import (
    ResourceType,
    Status,
)
from simple_health_checks.model import HealthCheckResponse
from simple_health_checks.resources.base import Resource

logger = logging.getLogger(__name__)


class HealthChecks:
    @staticmethod
    def get_module(name):
        resource = None

        try:
            package_name = "simple_health_checks.resources.{}".format(name)
            resource_class = import_module(package_name).resource
            if resource_class and issubclass(resource_class, Resource):
                resource = resource_class()
            else:
                resource = None
        except ImportError as exc:
            logger.error(exc)

        return resource

    def __init__(self):
        modules = {}
        for name in settings.RESOURCES:
            resource = HealthChecks.get_module(name)
            if resource:
                modules[resource.resource_name] = resource

        self.resources = modules

    def run(self, skip_resources=None, disable_cache=False):
        """
        Run all checks asynchronously and update their states
        We use pebble.ProcessPool to ensure that tasks are killed completely upon timeout
        This ensures we do not leave any locked processes hanging
        """
        skip_resources = skip_resources or []
        with ProcessPool(max_workers=settings.as_int("MAX_WORKERS")) as executor:
            futures_res = {
                executor.schedule(
                    res.check,
                    kwargs={
                        "skip_resources": skip_resources,
                        "disable_cache": disable_cache,
                    },
                    timeout=settings.as_int("TIMEOUT"),
                ): res
                for res in self.resources.values()
                if res.resource_name not in skip_resources
            }
        for future, resource in futures_res.items():
            try:
                resource.status = future.result()
            except concurrent.futures.TimeoutError:
                resource.set_status_timeout_or_error()
                logger.error(
                    "Resource %s failed to respond in time",
                    resource.resource_name,
                )
            except Exception as exc:  # pylint: disable=broad-except
                resource.set_status_timeout_or_error()
                logger.error(
                    "Resource %s check method raised an unexpected exception %s",
                    resource.resource_name,
                    exc,
                    exc_info=True,
                )
            resource.last_checked = time()

    def failed(self):
        """Convert and return any failed components"""

        self.run(skip_resources=[])

        return [str(res) for res in self.resources.values() if not res.ok]

    def to_dict(
        self,
        request_url,
        show_dependencies=False,
        skip_resources=None,
        disable_cache=False,
    ):
        """Convert to Serializer compatible object (for APIv2)"""
        skip_resources = skip_resources or []
        self.run(skip_resources, disable_cache)

        global_status = Status.OK

        dependencies = {"apis": [], "datastores": []}
        unavailable_components = []
        component_names = []

        for resource in self.resources.values():
            if resource.resource_name in skip_resources:
                continue
            component_names.append(resource.name)
            resource_type = resource.resource_type
            if resource_type == ResourceType.API:
                dependencies["apis"].append(resource.to_dict())
            elif resource_type == ResourceType.DATASTORE:
                dependencies["datastores"].append(resource.to_dict())

            if resource.status is not Status.OK:
                unavailable_components.append(resource.name)

            if resource.status < global_status:
                global_status = resource.status

        data = {
            "status": global_status.value,
            "datetime": datetime.utcnow(),
            "requestUrl": request_url,
            "serviceName": settings.SERVICE_NAME,
            "version": settings.SERVICE_VERSION,
            "simpleHealthChecksVersion": simple_health_checks.__version__,
            "components": component_names,
        }

        if global_status in [Status.DOWN, Status.DEGRADED, Status.NOT_CONFIGURED]:
            data["unavailableComponents"] = unavailable_components

        if show_dependencies:
            data["dependencies"] = dependencies

        response = HealthCheckResponse(**data)

        return response.dict(exclude_unset=True)


checks = HealthChecks()
