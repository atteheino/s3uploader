import os
import logging
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler
from s3uploader import upload

class MyHandler(FileSystemEventHandler):

    def __init__(self, bucket, profile, base_dir):
        self.bucket = bucket
        self.profile = profile
        self.base_dir = base_dir
        self.logger = logging.getLogger(__name__)

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        self.logger.info(event.src_path)
        self.logger.info(event.is_directory)
        self.logger.info(event.event_type)

        if(not event.is_directory):
            self.logger.info("Calling upload of " + event.src_path)
            upload(self.profile, self.bucket, event.src_path, self.base_dir)

#    def on_modified(self, event):
#        self.process(event)

    def on_created(self, event):
        self.process(event)