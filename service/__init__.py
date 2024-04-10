from loguru import logger
from . import cron_service
from configure import config


def init():
    # import cron_service
    if config.start_cron_job:
        cron_service.start_job()
    pass
