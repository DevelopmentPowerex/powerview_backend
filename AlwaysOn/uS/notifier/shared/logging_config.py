import logging

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def setup_logging(level: str = "INFO") -> None:
    level_value = getattr(logging, str(level).upper(), logging.INFO)

    logging.basicConfig(
        level=level_value,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
        force=True,  # asegura el formato aunque algo ya configuró logging
    )

    # opcional: reduce ruido de libs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)