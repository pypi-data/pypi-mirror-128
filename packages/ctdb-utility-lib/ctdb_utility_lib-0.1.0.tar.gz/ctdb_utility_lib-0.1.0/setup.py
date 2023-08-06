from setuptools import find_packages, setup

setup(
    name="ctdb_utility_lib",
    packages=find_packages(include=["ctdb_utility_lib"]),
    version="0.1.0",
    description="Contact Tracer DB Utility Python library",
    install_requires=["pytz"],
    author="Ahmed",
    license="MIT",
)