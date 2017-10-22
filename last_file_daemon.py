import argparse
import logging
import os
import uuid

import inotify.adapters
import yaml

_DEFAULT_LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

_LOGGER = logging.getLogger(__name__)

ROOT = "/home/nibz/Pictures"


def _configure_logging():
    _LOGGER.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()

    formatter = logging.Formatter(_DEFAULT_LOG_FORMAT)
    ch.setFormatter(formatter)

    _LOGGER.addHandler(ch)


def _main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Path to config file")
    args = parser.parse_args()
    config = yaml.safe_load(open(args.config))
    print(config)
    i = inotify.adapters.Inotify()

    for watch_dir in config['directories']:
        i.add_watch(bytes(watch_dir, 'utf-8'))

    try:
        for event in i.event_gen():
            if event is not None:
                (header, type_names, watch_path, filename) = event
                if 'IN_CLOSE_WRITE' in type_names:
                    _LOGGER.info("WD=(%d) MASK=(%d) COOKIE=(%d) LEN=(%d) MASK->NAMES=%s "
                                 "WATCH-PATH=[%s] FILENAME=[%s]",
                                 header.wd, header.mask, header.cookie, header.len, type_names,
                                 watch_path.decode('utf-8'), filename.decode('utf-8'))
                    name = watch_path.decode('utf-8') + "/" + filename.decode('utf-8')
                    uuid_target = watch_path.decode('utf-8') + "/." + str(uuid.uuid4())
                    os.symlink(name, uuid_target)
                    target = watch_path.decode('utf-8') + "/latest"
                    os.rename(uuid_target, target)

    finally:
        for watch_dir in config['directories']:
            i.remove_watch(watch_dir)

if __name__ == '__main__':
    _configure_logging()
    _main()
