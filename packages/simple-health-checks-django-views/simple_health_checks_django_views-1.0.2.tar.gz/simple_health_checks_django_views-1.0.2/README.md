## Django Views Plugin for Simple Health Checks

Provides 2 views that can be added to a django projects urls

Simply add the following to your urls file in your django project:

```python3
from simple_health_checks.urls import HEALTH_CHECK, PING

urlpatterns = [
    ...
    HEALTH_CHECK,
    PING,
]
```


Alternatively you can use the following but the middleware skip will not be active unless your 
ping url matches `HEALTH_CHECKS_PING_PATH`:

```python3
from simple_health_checks.views.views import HealthCheck, ping

urlpatterns = [
    ...
    url(r'^health/', HealthCheck.as_view(), name="health"),
    url(r'^ping/', ping, name="ping"),
]
```

To ensure that we skip middleware you MUST add `"simple_health_checks.middleware.SkipMiddlewarePing"` to 
the *top* of `MIDDLEWARE` in your django settings file.  


### Required environment variables

`HEALTH_CHECKS_CRITICAL_ON_PING` - used for resources that may hang when down but prevent the service from functioning.
This can be used to force a proxy that monitors this endpoint to display a service down error and prevent
future requests until it recovers. Comma separated resource names, matching the filename that defines the resource.

`HEALTH_CHECKS_TOKEN` - token used to gain access to more detailed information from the health endpoint

`HEALTH_CHECKS_PING_PATH` (Optional) - can be used to define a the ping uri if you wish to 
use `from simple_health_checks.urls import HEALTH_CHECK, PING` with a custom path

`HEALTH_CHECKS_HEALTH_PATH` (Optional) - can be used to define the health uri if you wish to use 
`from simple_health_checks.urls import HEALTH_CHECK, PING` with a custom path

`PING_PATH` is also used to ensure that when the ping endpoint is used we skip any django middleware that may 
try to communicate with a resource that may hang and cause an issue for the ping endpoint responding.
