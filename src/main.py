import argparse
import logging
from datetime import datetime
from sys import stdout

import telegram
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
    parser.add_argument('email')
    parser.add_argument('password')
    return parser.parse_args()


def is_verbosity_name_valid(name: str):
    if name not in _nameToLevel:
        raise argparse.ArgumentTypeError('Verbosity must be one of the following values: %s', ' '.join(_nameToLevel))
    return logging.getLevelName(name)


def main():
    arguments = get_arguments()
    _create_logger('yad2.log', arguments.verbosity)
    yad2 = Yad2(arguments.driver_path)

    if arguments.schedule:
        start_scheduler(arguments, yad2)
    else:
        start_bouncing(arguments, yad2)


def _create_logger(logfile: str, verbosity: int):
    logger_file_handler = logging.FileHandler(logfile, encoding='utf8')
    handler = logging.StreamHandler(stdout)
    handlers = [handler, logger_file_handler]
    logging.basicConfig(
        level=verbosity,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
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
