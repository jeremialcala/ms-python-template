# -*- coding: utf-8 -*-
"""
    This controller handles the service data lifecycle.

"""
import logging.config
import json
from inspect import currentframe
from functools import wraps

from classes import Settings, EventTransport
from constants import STARTING_AT, ENDING_AT
from utils import configure_logging

_set = Settings()
log = logging.getLogger(__name__)
logging.config.dictConfig(configure_logging())


def service_lifecycle(func):
    """
        This is a function that process messages outside the AMQP controller.
    :return: Response code with the result of this operation
    """
    log.info(STARTING_AT, currentframe().f_code.co_name)

    @wraps(func)
    def wrapper(*args, **kwargs):
        """
            This is a Wrapper is used to execute the lifecycle operations.
            With this tool we are going to make templates out of this code.

            TODO: Create the security module to deserialize a JWE message
            TODO: Separate all operation on different methods and use match to execute here
        :return:
        """
        log.info(STARTING_AT, currentframe().f_code.co_name)
        log.info(kwargs)
        if len(args) != 0:
            event = EventTransport(**json.loads(bytes.decode(args[3], "UTF-8")))
            log.info(event.body)

        log.info(ENDING_AT, currentframe().f_code.co_name)
        return func(*args, **kwargs)

    log.info(ENDING_AT, currentframe().f_code.co_name)
    return wrapper
