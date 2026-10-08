import logging
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOG_FOLDER = PROJECT_ROOT / "logs"
LOG_FILE = LOG_FOLDER / "mediguard.log"


def get_logger(name):
    """
    Create and return a configured logger for MediGuard.
    """
    LOG_FOLDER.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8",
    )

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger