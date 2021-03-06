""" Current version of the simcore_service_api_gateway application
"""
import pkg_resources

__version__ = pkg_resources.get_distribution("simcore_service_api_gateway").version

major, minor, patch = __version__.split(".")

api_version = __version__
api_vtag: str = f"v{major}"
