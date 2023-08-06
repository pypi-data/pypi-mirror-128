import time
from typing import Any, Callable, Dict, Tuple
from prometheus_client import Enum
from watchdog.observers import Observer
from watchdog.events import (
    FileClosedEvent,
    FileDeletedEvent,
    FileModifiedEvent,
    FileMovedEvent,
    FileSystemEventHandler,
    PatternMatchingEventHandler,
    FileCreatedEvent,
)
from watchdog.observers.api import ObservedWatch
from dataclasses import dataclass
from .lib.filesystem.fs_map import LocalFSResourceMap

from pydantic import BaseModel


class FSStatus(BaseModel):
    # placeholder for further future extension
    resource_id: str


class FSEvents(Enum):
    STATUS = Callable[[FSStatus], Any]
    # TODO: implement below.
    CREATED = "CREATED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"
    MOVED = "MOVED"


class FSEventBroker:
    event_listeners = {event_name.name: list() for event_name in FSEvents}

    def subscribe(self, event_name: FSEvents, fn) -> None:
        event_name = self._parse_enum(event_name)

        if event_name in self.event_listeners:
            self.event_listeners[event_name].append(fn)

    def unsubscribe(self, event_name: FSEvents, fn) -> None:
        event_name = self._parse_enum(event_name)

        if event_name in self.event_listeners:
            listeners = self.event_listeners[event_name]
            for idx, f in enumerate(listeners):
                if f == fn:
                    listeners.pop(idx)

    def dispatch(self, event_name: FSEvents, data) -> None:
        event_name = self._parse_enum(event_name)

        if event_name in self.event_listeners:
            for fn in self.event_listeners[event_name]:
                fn(data)

    def _parse_enum(self, event_name: FSEvents) -> str:
        if isinstance(event_name, FSEvents):
            return event_name.name
        return event_name


event_broker = FSEventBroker()


class FSEventHandler(PatternMatchingEventHandler):
    def __init__(self, local_fs_map: LocalFSResourceMap):
        super().__init__(ignore_directories=True)

        # dep inject local filesystem map
        self._res_map = local_fs_map

    def on_created(self, event: FileCreatedEvent) -> None:
        # add file to local fs map
        self._res_map.add_file(event.src_path)

        # dispatch new state
        event_broker.dispatch(FSEvents.STATUS, self._status)

    def on_modified(self, event: FileModifiedEvent) -> None:
        # update file in local fs map
        self._res_map.update_file(event.src_path)

        # dispatch new state
        event_broker.dispatch(FSEvents.STATUS, self._status)

    def on_deleted(self, event: FileDeletedEvent) -> None:
        # remove file from local fs map
        self._res_map.delete_file(event.src_path)

        # dispatch new state
        event_broker.dispatch(FSEvents.STATUS, self._status)

    def on_moved(self, event: FileMovedEvent) -> None:
        # update/add file in local fs map, remove file from local fs map
        self._res_map.delete_file(event.src_path)

        # NOTE: change in the future. Right now, this covers all cases.
        self._res_map.add_file(event.dest_path)
        self._res_map.update(event.dest_path)

        # dispatch new state
        event_broker.dispatch(FSEvents.STATUS, self._status)

    def on_closed(self, event: FileClosedEvent) -> None:
        # update file in local fs map
        self._res_map.update_file(event.src_path)

        # dispatch new state
        event_broker.dispatch(FSEvents.STATUS, self._status)

    # Helper methods
    @property
    def _status(self) -> FSStatus:
        return FSStatus(resource_id=self._res_map.resource_id)


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


if __name__ == "__main__":
    observers: Dict[str, ObserverWatcher] = dict()

    event_handler = FSEventHandler()
    observer = Observer()
    observer.start()

    try:
        while True:
            try:
                while True:
                    time.sleep(2)
                    print("work")

            except KeyboardInterrupt:
                watch_path = input()
                print(watch_path)

                if watch_path not in observers:
                    observer_watcher = observer.schedule(
                        event_handler, watch_path, recursive=True
                    )

                    # add watch path and ObservedWatcher object to dict of open observers
                    observers[watch_path] = observer_watcher

    except KeyboardInterrupt:
        observer.stop()
