from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    CFMID_PATH: Optional[str]
    CFMID_IMAGE: Optional[str]
    CFMID_HOST: Optional[str]
    CFMID_PORT: Optional[int]
