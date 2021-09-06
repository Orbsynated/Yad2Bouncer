import argparse
import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from sys import stdout

from apscheduler.schedulers.blocking import BlockingScheduler

from yad2 import Yad2

_nameToLevel = [
    'CRITICAL',
    'FATAL',
    'ERROR',
    'WARN',
    'WARNING',
    'INFO',
    'DEBUG',
    'NOTSET'
]


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--driver', required=False, dest='driver_path',
                        help='The driver must be supplied via PATH environment variable or via this argument')
    parser.add_argument('-s', '--schedule', required=False, action='store_true',
                        dest='schedule',
                        help='Whether to bounce automatically every 4 hours')
    parser.add_argument('-v', '--verbosity', required=False, dest='verbosity', type=is_verbosity_name_valid,
                        default=logging.INFO)
    parser.add_argument('--logs-path', required=False, dest='logs_path', type=Path, default=Path('../logs'))
    parser.add_argument('email')
    parser.add_argument('password')
    return parser.parse_args()


def is_verbosity_name_valid(name: str):
    if name not in _nameToLevel:
        raise argparse.ArgumentTypeError('Verbosity must be one of the following values: %s', ' '.join(_nameToLevel))
    return logging.getLevelName(name)


def main():
    arguments = get_arguments()
    _create_logger(arguments.logs_path, arguments.verbosity)
    yad2 = Yad2(arguments.driver_path)

    if arguments.schedule:
        start_scheduler(arguments, yad2)
    else:
        start_bouncing(arguments, yad2)


def _create_logger(logfile: Path, verbosity: int):
    log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
    # create folder for logs if not exists
    logfile.mkdir(parents=True, exist_ok=True)
    file_name = logfile.joinpath('yad2.log')
    logger_file_handler = RotatingFileHandler(str(file_name), encoding='utf8', mode='a', maxBytes=5 * 1024 * 1024)
    logger_file_handler.setFormatter(log_formatter)
    stdout_handler = logging.StreamHandler(stdout)
    stdout_handler.setFormatter(log_formatter)
    handlers = [stdout_handler, logger_file_handler]
    logging.basicConfig(
        level=verbosity,
        handlers=handlers,
    )


def start_bouncing(arguments, yad2):
    try:
        with yad2.login(arguments.email, arguments.password):
            yad2.bounce_all_ads()
    except:
        yad2.get_screenshot_as_file(
            'error_screenshot_{}.png'.format(datetime.now().strftime("%Y%m%dT%H%M%S"))
        )
        raise


def start_scheduler(arguments, yad2):
    scheduler = BlockingScheduler()
    scheduler.add_job(lambda: start_bouncing(arguments, yad2), 'interval', hours=4, minutes=5,
                      next_run_time=datetime.now())
    scheduler.start()


if __name__ == '__main__':
    main()
