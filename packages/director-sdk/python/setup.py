# coding: utf-8

"""
    Director API

    This is the oSparc's director API  # noqa: E501

    OpenAPI spec version: 1.0.0
    Contact: support@simcore.com
    Generated by: https://openapi-generator.tech
"""


from setuptools import setup, find_packages  # noqa: H301

NAME = "simcore-director-sdk"
VERSION = "1.0.0"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["urllib3 >= 1.15", "six >= 1.10", "certifi", "python-dateutil"]
REQUIRES.append("aiohttp")

setup(
    name=NAME,
    version=VERSION,
    description="Director API",
    author_email="support@simcore.com",
    url="https://github.com/ITISFoundation/osparc-simcore/tree/master/packages/director-sdk/python",
    keywords=["OpenAPI", "OpenAPI-Generator", "Director API"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description="""\
    This is the oSparc&#39;s director API  # noqa: E501
    """
)