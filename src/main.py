import logging
import logging.config
import getopt
import errno
import os
import sys
import time
import yaml
import s3uploader
from watchdog.observers import Observer
from filewatch_handler import MyHandler


def print_help():
    logging.info('main.py <command>')
    logging.info('Command may be: start, stop or status')

def main(argv):
    # Default interval of 60 sec.
    interval=60
    observer = Observer()
    
    pid = str(os.getpid())
    pidfile = "/tmp/s3uploader.pid"
 
    # Validate that we have only one command
    if len(argv) != 1:
        print_help()
        sys.exit()
    else:
        cmd = argv[0]
        # Start Service
        if cmd == 'start':
            config=load_config()
            interval=int(config['interval_sec'])
            if len(config['configurations']) > 0:
                logging.info("Start called.")
                if os.path.isfile(pidfile):
                    if pid_exists(int(get_pid_from_pidfile(pidfile))):
                        logging.info("%s already exists, exiting" % pidfile)
                        sys.exit()
                    else:
                        logging.info("Removing stale PID file. Process does not exists anymore.")
                        os.unlink(pidfile)
                open(pidfile, 'w').write(pid)

                for configuration in config['configurations']:
                    create_observer_instance(
                        configuration['name'],
                        configuration['directory'],
                        configuration['boto_profile'],
                        configuration['bucket'],
                        observer
                    )

                observer.start()

                try:
                    while True:
                        time.sleep(interval)
                except KeyboardInterrupt:
                    observer.stop()
                    os.unlink(pidfile)
                observer.join()
        # Stop Service
        elif cmd == 'stop':
            logging.info("Stop called")
            observer.unschedule_all()
            observer.stop()
            os.unlink(pidfile)
        # Status query
        elif cmd == 'status':
            logging.info("Status called")
            if os.path.isfile(pidfile):
                if pid_exists(int(get_pid_from_pidfile(pidfile))):
                    logging.info( "Service is running.")
                else:
                    logging.info( "Service is not running.")
            else:
                logging.info( "Service is not running.")
        else:
            sys.exit('Unknown command "%s".' % cmd)

def create_observer_instance(
    name,
    directory,
    profile,
    bucket,
    observer
):
    # Validate that we have all necessary parameters
    if directory == "" or profile == "" or bucket == "":
        logging.info(directory)
        logging.info(profile)
        logging.info(bucket)
        print_help()
        sys.exit()
    else:
        logging.info("Creating observer for %s" % name)
        logging.info("Directory: %s" % directory)
        logging.info("Uploading already present files...")
        s3uploader.upload_files_from_directory(profile, bucket, directory)
        logging.info("...Done uloading from %s" % directory)
        
        observer.schedule(MyHandler(bucket, profile, directory), path=directory, recursive=True)

def pid_exists(pid):
    """Check whether pid exists in the current process table.
    UNIX only.
    """
    if pid < 0:
        return False
    if pid == 0:
        # According to "man 2 kill" PID 0 refers to every process
        # in the process group of the calling process.
        # On certain systems 0 is a valid PID but we have no way
        # to know that in a portable fashion.
        raise ValueError('invalid PID 0')
    try:
        os.kill(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # ESRCH == No such process
            return False
        elif err.errno == errno.EPERM:
            # EPERM clearly means there's a process to deny access to
            return True
        else:
            # According to "man 2 kill" possible error values are
            # (EINVAL, EPERM, ESRCH)
            raise
    else:
        return True

def get_pid_from_pidfile(pidfile):
    try:
        file = open(pidfile) 
        return file.read()
    except:
        sys.exit("Could not read PID file")

def setup_logging(
    default_path='resources/logging.conf.yml',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def load_config(default_path='../conf/s3uploader.conf.yml'):
    path=default_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
            return config
    else:
        sys.exit("Configuration file not found")

if (__name__ == '__main__'):
    setup_logging()
    main(sys.argv[1:])
