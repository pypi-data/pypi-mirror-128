from dynaconf import Validator

validators = [
    Validator("CRITICAL_ON_PING", default=[]),
    Validator("HEALTH_PATH", default="health/1/"),
    Validator("PING_PATH", default="ping/1/"),
    Validator("TOKEN", default="health-checks-token"),
]
