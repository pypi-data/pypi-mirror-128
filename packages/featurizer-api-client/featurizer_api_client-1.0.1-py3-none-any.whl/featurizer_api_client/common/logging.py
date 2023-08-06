import os
import logging
import importlib
from pathlib import Path


def get_client_logger(config):
    """Gets the client logger"""

    # Load the configuration
    logger = logging.getLogger("client_logger")

    # Make sure the logging directory exists
    if config.get("kwargs", {}).get("filename"):
        Path(os.path.join(os.path.dirname(config.get("kwargs").get("filename")))).mkdir(parents=True, exist_ok=True)

    # Prepare the logging module and logger class name
    logger_path = config["class"].split(".")
    logger_module, logger_class = ".".join(logger_path[:-1]), logger_path[-1]

    # Prepare the logging class
    logger_class = getattr(importlib.import_module(logger_module), logger_class)

    # Prepare the handler
    handler = logger_class(**config["kwargs"])

    # Configure the logger level
    logger.setLevel(logging.DEBUG)

    # Configure the formatter
    formatter = logging.Formatter("%(asctime)s, %(message)s")
    handler.setFormatter(formatter)

    # Register the logger
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # Return the logger
    return logger
