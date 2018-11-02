""" user's session

    - stores user-specific data into a session object
    - session object has a dict-like interface
    - installs middleware in ``aiohttp.web.Application`` that attaches to
    a session object to ``request``. Usage
    ```
        async def my_handler(request)
            session = await get_session(request)
    ```
    - data sessions stored in encripted cookies.
        - client tx/rx session's data everytime (middleware?)
        - This way, we can scale in theory server-side w/o issues
        - TODO: test and demo statement above
    - based in aiotthp_session library : http://aiohttp-session.readthedocs.io/en/latest/

    TODO: check storing JSON-ed data into redis-service, keeping into cookie only redis key (random UUID). Pros/cons analysis.
"""

import base64
import logging

import aiohttp_session
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from cryptography import fernet

from .settings import APP_CONFIG_KEY

log = logging.getLogger(__file__)

def setup(app):
    """
        Inits and registers a session middleware in aiohttp.web.Application
    """
    log.debug("Setting up %s ...", __name__)

    secret_key = app[APP_CONFIG_KEY].get("SECRET_KEY")
    if secret_key is None:
        # secret_key must be 32 url-safe base64-encoded bytes
        fernet_key = fernet.Fernet.generate_key()
        secret_key = base64.urlsafe_b64decode(fernet_key)
        app[APP_CONFIG_KEY]["SECRET_KEY"] = secret_key

    storage = EncryptedCookieStorage(secret_key, cookie_name="API_SESSION")
    aiohttp_session.setup(app, storage)


# alias
get_session = aiohttp_session.get_session
setup_session = setup


__all__ = (
    'setup_session',
    'get_session'
)