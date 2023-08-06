__title__ = 'Amino.ed'
__author__ = 'Alert Aigul'
__license__ = 'MIT'
__copyright__ = 'Copyright 2020-2021 Alert'
__version__ = '2.1.0'

from asyncio import get_event_loop
from requests import get

import sync
from .global_client import Client
from .community_client import CommunityClient
from .utils import exceptions, models, types, helpers


def run_with_client(deviceId: str = None):
    async def start(callback):
        async with Client(deviceId) as client:
            await callback(client)

    def _main(callback):
        loop = get_event_loop()
        loop.run_until_complete(start(callback))
    return _main


__newest__ = get("https://pypi.python.org/pypi/Amino.ed/json").json()["info"]["version"]

if __version__ != __newest__:
    print(f"New version available: {__newest__} (Using {__version__})")
    print(f"Visit our discord server: https://discord.gg/rbgq5TtWEA\n")
