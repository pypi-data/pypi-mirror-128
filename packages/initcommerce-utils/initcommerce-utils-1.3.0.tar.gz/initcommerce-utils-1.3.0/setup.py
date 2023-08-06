from setuptools import find_packages, setup

from initcommerce import __author__, __author_email__, __description__, __version__

NAME = "initcommerce-utils"
VERSION = __version__
AUTHOR = __author__
AUTHOR_EMAIL = __author_email__
MAINTAINER = AUTHOR
MAINTAINER_EMAIL = AUTHOR_EMAIL
with open("requirements.txt") as f:
    DEPENDENCIES = [line.strip("\n") for line in f.readlines()]

EXTRAS = {
    "db": [
        "alembic~=1.7",
        "sqlalchemy[mysql,mysql_connector]~=1.4.25",
    ],
    "cache": [
        "aioredis~=2.0",
    ],
    "email-sender": [
        "sendgrid~=6.9",
    ],
    "jwt": [
        "pyjwt[crypto]~=2.3",
    ],
    "message-queue": [
        "aio-pika~=6.8",
    ],
    "object-storage": [
        "minio~=7.1",
    ],
    "phonenumbers": [
        "phonenumbers~=8.12",
    ],
    "sms-sender": [
        "twilio~=7.3",
    ],
}

setup(
    name=NAME,
    version=str(VERSION),
    description=__description__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    url="https://github.com/initCommerce/backend-utils",
    download_url="https://pypi.org/project/initcommerce-utils",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Utilities",
    ],
    license="BSD 3-Clause",
    license_file="LICENSE",
    install_requires=DEPENDENCIES,
    extras_require=EXTRAS,
)
