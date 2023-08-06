import os
import sys
import inspect
import rich.pretty
from loguru import logger

# -- Define the metadata.
try:
    from importlib import metadata
except ImportError: # When Python < 3.8
    import importlib_metadata as metadata
__version__ = metadata.version("pyhelios")
__description__ = "The Helios' toolbox"
__maintainers__ = ["Julien Vanharen <julien.vanharen@gmail.com>"]

# -- Configure the rich package.
rich.pretty.install()

# -- Configure le loguru package.
config = {
    "handlers": [
        {
            "sink": sys.stderr,
            "filter": lambda record: record["level"].name == "ERROR",
            "format": "<g>[{time:HH:mm:ss}]</g> <lvl>[{level}]</lvl> <lvl>{message}</lvl> <cyan>{name}</cyan>:<magenta>{line}</magenta>",
        },
        {
            "sink": sys.stdout,
            "filter": lambda record: record["level"].name == "INFO",
            "format": "<g>[{time:HH:mm:ss}]</g> <lvl>[{level}]</lvl> {message}",
        },
    ]
}
logger.configure(**config)
logger.level("ERROR", color="<red>")
logger.level("INFO", color="<green>")
