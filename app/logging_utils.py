import logging


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for the given name.

    Args:
        name: Usually __name__ from the calling module

    Returns:
        Configured logger instance

    """
    return logging.getLogger(name)


def log_request_data(
    logger: logging.Logger, data: dict | str, endpoint: str = ''
) -> None:
    """
    Helper function to log request data consistently.

    Args:
        logger: Logger instance to use
        data: Request data to log
        endpoint: Optional endpoint name for context

    """
    if endpoint:
        logger.info('Request to %s: %s', endpoint, data)
    else:
        logger.info('Request data: %s', data)


def log_error(logger: logging.Logger, error: Exception, context: str = '') -> None:
    """
    Helper function to log errors consistently.

    Args:
        logger: Logger instance to use
        error: Exception that occurred
        context: Optional context information

    """
    if context:
        logger.error('Error in %s: %s', context, str(error))
    else:
        logger.error('Error occurred: %s', str(error))
