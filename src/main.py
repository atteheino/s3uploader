import getopt
import errno
import os
import sys
import time
import s3uploader
from watchdog.observers import Observer
from filewatch_handler import MyHandler


def print_help():
    print('main.py [options] <command>')
    print('options: -d <directory to watch> -b <bucket where to upload> -p <boto profile> -i <polling interval in seconds>')
    print('Command may be: start, stop or status')

def main(argv):

    profile=''
    bucket=''
    directory=''
    # Default interval of 60 sec.
    interval=60

    pid = str(os.getpid())
    pidfile = "/tmp/s3uploader.pid"

    # Get parameters and assign to variables
    try:
        opts, args = getopt.getopt(argv,"hp:d:b:i:",["--help","--profile=","--directory=","--bucket=","--interval="])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ("-p", "--profile"):
            profile = arg
        elif opt in ("-b", "--bucket"):
            bucket = arg
        elif opt in ("-d", "--directory"):
            directory = arg
        elif opt in ("-i", "--interval"):
            interval = int(arg)
 
    # Validate that we have all necessary parameters and only one command
    if len(args) != 1 or directory == "" or profile == "" or bucket == "":
        print(args)
        print(directory)
        print(profile)
        print(bucket)
        print_help()
        sys.exit()
    else:
        cmd = args[0]
        # Start Service
        if cmd == 'start':
            print("Start called.")
            if os.path.isfile(pidfile):
                if pid_exists(get_pid_from_pidfile(pidfile)):
                    print("%s already exists, exiting" % pidfile)
                    sys.exit()
                else:
                    print("Removing stale PID file. Process does not exists anymore.")
                    os.remove(pidfile)


            open(pidfile, 'w').write(pid)
            print("Uploading already present files...")
            s3uploader.upload_files_from_directory(profile, bucket, directory)
            print("...Done")
            observer = Observer()
            observer.schedule(MyHandler(bucket, profile, directory), path=directory, recursive=True)
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
            print("Stop called")
            observer.stop()
            os.unlink(pidfile)
        # Status query
        elif cmd == 'status':
            print("Status called")
            if os.path.isfile(pidfile):
                print( "Service is running.")
            else:
                print( "Service is not running.")
        else:
            sys.exit('Unknown command "%s".' % cmd)

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

if (__name__ == '__main__'):
    main(sys.argv[1:])
