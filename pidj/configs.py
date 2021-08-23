"""PiDJ configuration settings."""
from environs import Env

_env: Env = Env()
_env.read_env()

# Keep this in a .env file in project root dir i.e.: CLIENT_ID=keyvalue
CLIENT_ID: str = _env.str("CLIENT_ID", default='keep-in-.env-file')
"""Spotify Client ID"""

CLIENT_SECRET: str = _env.str("CLIENT_SECRET", default='keep-in-.env-file')
"""Spotify Client Secret Key"""

SESSIONS_SECRET: str = _env.str("SESSIONS_SECRET", default='keep-in-.env-file')
"""Flask Sessions Secret Key"""
