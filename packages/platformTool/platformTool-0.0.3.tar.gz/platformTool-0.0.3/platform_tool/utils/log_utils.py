#!/user/bin/env python3
# -*- coding: utf-8 -*-
"""
--------------------------------------
    Author:     JiChao_Song
    Date  :     2021/11/11 21:27
    Desc  :     日志工具
--------------------------------------
"""
from loguru import logger


class LoggerFactory:

    def __init__(self, BASE_DIR):

        logger.add(f"{BASE_DIR}/logs/app.log", rotation = "00:00", retention="10 days",
                   encoding = 'utf-8', enqueue=True)
        logger.add(f"{BASE_DIR}/logs/error.log", rotation = "00:00", retention="10 days", level = 'ERROR',
                   encoding = 'utf-8', backtrace=True)
        logger.add(f"{BASE_DIR}/logs/debug.log", rotation = "00:00", retention="10 days", level = 'DEBUG',
                   encoding = 'utf-8', backtrace=True)
        logger.add(f"{BASE_DIR}/logs/warning.log", rotation = "00:00", retention="10 days", level = 'WARNING',
                   encoding = 'utf-8', backtrace=True)
        self.logger = logger

