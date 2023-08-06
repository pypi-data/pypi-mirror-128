try:
    from django.conf.urls import re_path as url
except:  # pylint: disable=bare-except
    from django.conf.urls import url

from simple_health_checks.config import settings
from simple_health_checks.views.views import (  # pylint: disable=import-error
    HealthCheck,
    ping,
)

HEALTH_CHECK = url(
    r"^{}".format(settings.HEALTH_PATH), HealthCheck.as_view(), name="health"
)
PING = url(r"^{}".format(settings.PING_PATH), ping, name="ping")

urlpatterns = [HEALTH_CHECK, PING]
