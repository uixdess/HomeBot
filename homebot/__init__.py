"""Homebot module."""

__version__ = "2.1.0"

from dotenv import load_dotenv
import os
from pathlib import Path

bot_path = Path(__file__).parent
modules_path = bot_path / "modules"

modules = []

get_config = os.environ.get

load_dotenv("config.env")
