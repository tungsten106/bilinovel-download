import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Union


def init_log(
        log_folder: Union[str, Path],
        level: str = 'INFO',
        reserve_day: int = 90
    ) -> None:
    """
    初始化日志记录系统，每天新建一个日志文件（日志过少时不会新建）进行日志保存。
    日志文件Handler会添加到根Logger，因此任何其它使用logging的库（如flask）
    的日志也会保存到日志文件中。

    Parameters
    ----------
    log_folder : Union[str, Path]
        日志保存的位置，可以直接以字符串'a/b/c'的形式指定，不需要事先存在。
    level : str, optional
        日志等级, by default 'INFO'
    reserve_day : int, optional
        日志文件保留时间, by default 90
    """

    log_folder = Path(log_folder)
    log_folder.mkdir(parents=True, exist_ok=True)

    time_rotating_hdlr = TimedRotatingFileHandler(
        filename=str(log_folder / 'run.log'), when='d', backupCount=reserve_day
    )
    time_rotating_hdlr.setFormatter(
        logging.Formatter(
            '%(asctime)s [%(name)s - %(funcName)s] %(levelname)s %(message)s'
        )
    )
    root_logger = logging.getLogger()
    root_logger.addHandler(time_rotating_hdlr)
    root_logger.setLevel(level)
    _logger = logging.getLogger(__name__)
    _logger.info('init log system')
    _logger.info(f"log level: {_logger.level}")


def get_uvicorn_cfg(level: str = 'INFO') -> dict:
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
        },
        "loggers": {
            "uvicorn": {"handlers": [], "level": level},
            "uvicorn.error": {"handlers": ["default"], "level": "INFO"},
            "uvicorn.access": {"handlers": [], "level": level}
        },
    }
