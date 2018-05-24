from datetime import datetime
from pathlib import Path


class PlainSnapShot:
    def __init__(self, stats, stability_map):
        self.stats = stats
        self.stability_map = stability_map


class SnapShot:
    def __init__(
            self,
            root_path,
            glob,
            old_snapshot=None,
            stability_threshold=1,
    ):

        self.time = datetime.now()
        self._root_path_str = root_path
        self.root_path = Path(root_path)
        self.old_snapshot = old_snapshot or self
        self.stability_threshold = stability_threshold
        self._glob = glob
        self.paths = list(self.root_path.glob(self._glob))

        self.stats = {path: path.stat() for path in self.paths}

        self.created_paths = self._get_created()
        self.created = self._get_created()
        self.modified = self._get_modified()
        self.deleted = self._get_deleted()
        self.stability_map = {
            path: self._get_stability(path)
            for path in self.paths
        }
        self.stabilized = self._get_stabilized()

    def _get_created(self):
        return self.stats.keys() - self.old_snapshot.stats.keys()

    def _get_commons(self):
        return self.stats.keys() & self.old_snapshot.stats.keys()

    def _is_modified(self, path):
        return (self.stats[path].st_mtime !=
                self.old_snapshot.stats[path].st_mtime)

    def _get_modified(self):
        return filter(self._is_modified, self._get_commons())

    def _get_deleted(self):
        return self.old_snapshot.stats.keys() - self.stats.keys()

    def _get_stability(self, path):
        return self.time.timestamp() - self.stats[path].st_mtime

    def _get_stabilized(self):
        return [
            path for path, stability in self.stability_map.items()
            if self.old_snapshot.stability_map[path] < self.stability_threshold
            and stability >= self.stability_threshold
        ]

    def plain(self):
        return PlainSnapShot(self.stats, self.stability_map)

    def next(self):
        return SnapShot(
            root_path=self._root_path_str,
            glob=self._glob,
            old_snapshot=self.plain(),
            stability_threshold=self.stability_threshold,
        )

    def iter_events(self):
        for path in self.created:
            yield {
                'event_type': 'created',
                'path': path,
                'stats': self.stats[path]
            }

        for path in self.modified:
            yield {
                'event_type': 'modified',
                'path': path,
                'stats': self.stats[path]
            }

        for path in self.deleted:
            yield {
                'event_type': 'deleted',
                'path': path,
                'stats': self.stats[path]
            }

        for path in self.stabilized:
            yield {
                'event_type': 'stabilized',
                'path': path,
                'stats': self.stats[path]
            }
