from dataclasses import dataclass
from watchdog.events import FileSystemEventHandler
from watchdog.observers.api import ObservedWatch
from typing import Tuple


@dataclass
class ObserverWatcher:
    event_handler: FileSystemEventHandler
    watch: ObservedWatch

    @classmethod
    def create_observer(
        cls, event_handler: FileSystemEventHandler, path: str, recursive: bool
    ):
        """Convenience method for creating a new observer"""
        watcher = ObservedWatch(path, recursive)
        return cls(event_handler=event_handler, watch=watcher)

    def as_tuple(self) -> Tuple[FileSystemEventHandler, ObservedWatch]:
        """Convenience method that returns object as deconstructed tuple"""
        return self.event_handler, self.watch
