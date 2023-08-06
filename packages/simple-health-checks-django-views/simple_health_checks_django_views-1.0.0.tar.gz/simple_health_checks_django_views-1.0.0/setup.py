import os

from setuptools import setup

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "./VERSION"), "r", encoding="utf-8") as version_file:
    version = str(version_file.readline()).strip()

setup(
    name="simple_health_checks_django_views",
    version=version,
    description="Django views plugin for simple-health-checks,"
    " adds endpoints for ping and health checks",
    url="https://gitlab.com/genomicsengland/opensource/simple-healthchecks",
    author="Nicholas Dentandt, Oleg Gerasimenko, Constantina Polycarpou",
    author_email="noreply@genomicsengland.co.uk",
    license="Apache License 2.0",
    license_files=("LICENSE",),
    long_description="file: README.md",
    long_description_content_type="text/markdown",
    packages=[
        "simple_health_checks.views",
        "simple_health_checks.serializers",
        "simple_health_checks.additional_configs",
        "simple_health_checks",
    ],
    install_requires=[
        "simple_health_checks",
        "Django",
        "djangorestframework",
    ],
    extras_require={
        "tests": ["simple_health_checks[tests]"],
        "dev": ["simple_health_checks[dev]"],
    },
)
