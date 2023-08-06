from watchdog.events import FileSystemEventHandler

from .lib.filesystem.events.observer import ObserverWatcher
from .lib.filesystem.fs_resource_map import LocalFSResourceMap


class FSObserverWatcher(ObserverWatcher):
    @classmethod
    def from_local_fs_resource_map(
        cls,
        event_handler: FileSystemEventHandler,
        fs_resource_map: LocalFSResourceMap,
        recursive: bool = True,
    ):
        """Convenience method for creating a new observer from a LocalFSResourceMap instance"""
        return cls.create_observer(
            event_handler, fs_resource_map.data_path, recursive=recursive
        )
