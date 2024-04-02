from loguru import logger
from . import cron_service


def init():
    # import cron_service
    cron_service.start_job()
    pass
