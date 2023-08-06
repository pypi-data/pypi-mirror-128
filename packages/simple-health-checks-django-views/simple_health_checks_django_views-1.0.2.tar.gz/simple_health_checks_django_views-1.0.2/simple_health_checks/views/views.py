import logging

from django.http import (
    HttpResponse,
    JsonResponse,
)
from pebble import ProcessPool
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView

from simple_health_checks.config import settings
from simple_health_checks.enums import Status
from simple_health_checks.health_checks import checks as health_checks
from simple_health_checks.serializers.health_checks import (  # pylint: disable=import-error
    HealthCheckSerializer,
)

logger = logging.getLogger(__name__)


def ping(_):  # pylint: disable=unused-argument
    """
    CRITICAL_ON_PING is used for resources that may hang when down but prevent
    the service from functioning. This can be used to force a proxy that monitors
    this endpoint to display a service down error and prevent future requests until
    it recovers.
    """
    critical_on_ping = []
    for name in settings.CRITICAL_ON_PING:
        if name in health_checks.resources:
            critical_on_ping.append(health_checks.resources[name])

    if critical_on_ping:
        with ProcessPool(max_workers=2) as executor:
            futures_res = {
                executor.schedule(
                    res.check,
                    kwargs={
                        "disable_cache": True,
                    },
                    timeout=settings.as_int("TIMEOUT"),
                ): res
                for res in critical_on_ping
            }
            for future, res in futures_res.items():
                try:
                    status = future.result()
                    if status != Status.OK:
                        raise Exception(
                            "Resource %s is unavailable" % res.resource_name
                        )
                except Exception:  # pylint: disable=broad-except
                    logger.error(
                        "Resource %s is unavailable",
                        res.resource_name,
                        exc_info=True,
                    )
                    return HttpResponse(status=503)

    pong = {"ping": "pong"}
    return JsonResponse(pong)


@permission_classes((permissions.AllowAny,))
class HealthCheck(APIView):
    serializer = HealthCheckSerializer

    def get(self, request):
        data = health_checks.to_dict(
            request.build_absolute_uri(),
            show_dependencies=self.display_extra,
            skip_resources=self.skip_resources,
            disable_cache=self.disable_cache,
        )
        result = self.serializer(data=data)

        result.is_valid(raise_exception=True)
        if result.data["status"] == Status.DOWN.value:
            return JsonResponse(result.data, status=503)

        return JsonResponse(result.data)

    @property
    def display_extra(self):
        token = self.request.GET.get("token")
        return token == settings.TOKEN

    @property
    def skip_resources(self):
        skip = self.request.GET.get("skip")

        skip_resources = skip.lower().replace("%20", " ").split(",") if skip else []

        # Avoid loops by always skipping the service requesting the health check
        skip_resources.append(settings.SERVICE_NAME.lower())
        return list(set(skip_resources))

    @property
    def disable_cache(self):
        disable_cache = self.request.GET.get("disable_cache")
        return disable_cache is not None and disable_cache.lower() == "true"
