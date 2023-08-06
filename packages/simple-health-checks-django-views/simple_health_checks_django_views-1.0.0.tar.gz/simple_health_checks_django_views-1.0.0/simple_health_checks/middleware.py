from simple_health_checks.config import settings
from simple_health_checks.views.views import ping  # pylint: disable=import-error


class SkipMiddlewarePing:  # pylint: disable=too-few-public-methods
    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        """
        Skips middleware only for the ping endpoint. This prevents any database queries from being
        executed and prevents timing out of the endpoint when the replica DB is down.
        This middleware must be added to the top of MIDDLEWARE in your settings.py file
        """
        if request.path == f"/{settings.PING_PATH}":
            return ping(request)
        response = self.get_response(request)
        return response
