import logging

logger = logging

logger.basicConfig(level=logger.INFO,
    format='%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s',
        handlers=[logger.FileHandler("hello_flask.log", mode='w'),
        logger.StreamHandler()])
stream_handler = [h for h in logger.root.handlers if isinstance(
    h, logger.StreamHandler)][0]
stream_handler.setLevel(logger.INFO)