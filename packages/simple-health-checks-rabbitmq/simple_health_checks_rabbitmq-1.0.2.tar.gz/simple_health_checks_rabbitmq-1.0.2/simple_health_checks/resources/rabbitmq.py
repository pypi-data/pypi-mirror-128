import logging
from time import time

from kombu import Connection

from simple_health_checks.config import settings
from simple_health_checks.enums import (
    ResourceType,
    Status,
)
from simple_health_checks.resources.base import Resource

logger = logging.getLogger(__name__)


class RabbitMQ(Resource):
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.name = "RabbitMQ"
        self.connection_type = "OTHER"
        self.can_skip = False
        self.resource_type = ResourceType.DATASTORE

        self.is_configured = bool(settings.RABBITMQ_BROKER_URL)
        if self.is_configured:
            self.url = settings.RABBITMQ_BROKER_URL

        super().__init__(filename=__file__)

    def check(self, skip_resources=None, disable_cache=False):
        if self.use_cached_data(disable_cache):
            return self.status

        status = self.failed_status

        try:
            conn = Connection(
                self.url,
                connect_timeout=2,
                transport_options={"visibility_timeout": 2},
                heartbeat=1,
            )
            conn.ensure_connection(max_retries=2, interval_max=1, interval_start=0)
            status = Status.OK
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(exc)

        self.status = status
        self.last_checked = time()
        return self.status


resource = RabbitMQ
