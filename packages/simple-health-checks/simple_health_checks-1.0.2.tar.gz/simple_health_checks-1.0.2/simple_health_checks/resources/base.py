import logging
import os
from time import time

import requests

from simple_health_checks.config import settings
from simple_health_checks.enums import (
    ResourceType,
    Status,
)

logger = logging.getLogger(__name__)


class Resource:
    """Abstract class for the resource"""

    name = ""
    resource_name = ""
    description = ""
    can_skip = False
    is_configured = False
    resource_type = None
    last_checked = None
    url = None
    health_path = ""
    connection_type = None
    status = None
    affected = []  # list of affected parts of code (user facing)

    def __init__(self, filename=__file__):
        if not self.is_configured:
            self.status = Status.NOT_CONFIGURED
        else:
            self.validate_setup()
        self.resource_name = os.path.basename(filename).replace(".py", "").lower()

    def __str__(self):
        return (
            f"[Health] {self.name}({self.connection_type}) Status: {self.status.value}"
        )

    def to_dict(self, *args, **kwargs):
        additional_properties = {}

        res = {
            "status": self.status.value,
            "type": self.connection_type,
            "description": self.name,
            "url": [self.safe_url] if self.url else [],
        }

        if self.health_path:
            additional_properties["healthPath"] = self.health_path

        if not self.ok and self.affected:
            additional_properties["affected"] = ",".join(self.affected)

        if additional_properties:
            res["additionalProperties"] = additional_properties

        return res

    def use_cached_data(self, disable_cache):
        should_use_cache = False
        if (
            not disable_cache
            and self.last_checked
            and time() - self.last_checked < settings.as_int("CACHE_SECONDS")
        ):
            logger.debug(
                "Not running health check for resource %s, using cached data", self.name
            )
            should_use_cache = True

        return should_use_cache

    def set_status_timeout_or_error(self):
        """ Resource did not respond within timeout """
        self.status = self.failed_status

    @property
    def ok(self):
        return self.status == Status.OK

    @property
    def failed_status(self):
        return (
            Status.DOWN
            if (self.resource_name in settings.CRITICAL)
            else Status.DEGRADED
        )

    def validate_setup(self):
        """Check if child classes are configured"""

        assert self.name
        assert self.resource_type
        assert self.url
        assert self.connection_type

    def check(self, skip_resources=None, disable_cache=False):
        raise NotImplementedError()

    @property
    def safe_url(self):
        """Return URL without auth part"""

        if self.url:
            return self.url.split("@")[1] if "@" in self.url else self.url
        return None


class SimpleHTTPResource(Resource):
    """Abstract REST Resource check"""

    health_path = ""  # relative path to the simple_health_checks endpoint
    method = "GET"
    resource_type = ResourceType.API

    def __init__(self, *args, **kwargs):
        self.connection_type = "REST"
        super().__init__(*args, **kwargs)

    @property
    def headers(self):
        return {
            "HTTP_USER_AGENT": "simple_health_checks service:{}".format(
                settings.SERVICE_NAME
            )
        }

    @property
    def request_params(self):
        return {}

    def check(self, skip_resources=None, disable_cache=False):
        if not self.is_configured:
            # Don't run check if it's not configured
            logger.warning(f"{self.name} resource is not configured for health checks")
            return self.status

        if self.use_cached_data(disable_cache):
            return self.status

        query_params = ""

        if self.can_skip and skip_resources:
            if "?" in self.health_path:
                query_params += "&skip="
            else:
                query_params += "?skip="
            query_params += ",".join(skip_resources)

        if self.can_skip and disable_cache is True:
            if "?" in query_params or "?" in self.health_path:
                query_params += "&disable_cache=true"
            else:
                query_params += "?disable_cache=true"

        _status = self.failed_status
        try:
            url = f"{self.url}{self.health_path}{query_params}"
            with requests.request(
                self.method,
                url,
                headers=self.headers,
                timeout=settings.as_int("TIMEOUT"),
                **self.request_params,
                stream=True,
            ) as response:
                if response.ok:
                    _status = Status.OK
                # pylint: disable=assignment-from-none
                post_check_status = self.post_check(response)
            if post_check_status:
                _status = post_check_status
        except Exception as error:  # pylint: disable=broad-except
            logger.error(error)
            _status = self.failed_status

        self.status = _status
        self.last_checked = time()

        return self.status

    def post_check(self, response):  # pylint: disable=unused-argument,no-self-use
        """Check the response body and return new status

        :param response: `requests` Response object
        :return: Status value or None
        """

        return None


resource = None
