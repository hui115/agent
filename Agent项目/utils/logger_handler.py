import logging
import os
from path_tool import get_abs_path
LOG_ROOT=get_abs_path("log")
os.makedirs(LOG_ROOT,exist_ok=True)

DEFUALT_LOG_FROMAT=logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s'
)
def get_logger(
        name:str='agent',
        console_level:int=logging.INFO,
        file_level=logging.DEBUG,
        log_file=None
)->logging.Logger:
    logger=logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #控制台Handler
    console_handler=logging.StreamHandler()
    console_handler.setLevel()

