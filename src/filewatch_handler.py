from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):

    def process(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        print(event.src_path)
        print(event.is_directory)
        print(event.event_type)

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)

