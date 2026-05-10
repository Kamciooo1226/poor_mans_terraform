import sys

from loguru import logger


def setup_logging():
    logger.remove()
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:MM:SS}</green> | <level>{level}</level> | {message}",
        level="DEBUG",
        enqueue=True,
        colorize=True,
    )
    logger.add(
        "logs/app.jsonl",
        rotation="10 MB",
        format="{time:YYYY-MM-DD HH:MM:SS} | {level} | {message}",
        level="INFO",
        serialize=True,
        enqueue=True,
    )
