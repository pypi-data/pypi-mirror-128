import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def dotenv(key: str) -> Optional[str]:
    return os.getenv(key)
