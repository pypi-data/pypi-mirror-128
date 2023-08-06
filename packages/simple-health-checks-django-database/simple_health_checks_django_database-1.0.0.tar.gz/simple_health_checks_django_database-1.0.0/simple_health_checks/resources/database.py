import logging
from time import time

from django.conf import settings as django_settings
from django.db import (
    OperationalError,
    connection,
)

from simple_health_checks.enums import (
    ResourceType,
    Status,
)
from simple_health_checks.resources.base import Resource

logger = logging.getLogger(__name__)


class DjangoDatabase(Resource):
    # pylint: disable=too-many-instance-attributes

    def __init__(self):
        self.name = "Database"
        self.connection_type = "OTHER"
        self.can_skip = False
        self.resource_type = ResourceType.DATASTORE
        self.is_configured = True

        try:
            self.url = django_settings.DATABASE_HOST
        except AttributeError:
            self.url = django_settings.DATABASE_URL

        super().__init__(filename=__file__)

    def check(self, skip_resources=None, disable_cache=False):
        if self.use_cached_data(disable_cache):
            return self.status

        status = self.failed_status

        try:
            connection.ensure_connection()
            status = Status.OK
        except OperationalError as err:
            logger.error(err, exc_info=True)

        self.status = status
        self.last_checked = time()
        return self.status


resource = DjangoDatabase
