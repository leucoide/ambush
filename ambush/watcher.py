from .snapshot import SnapShot


class Watcher:
    def __init__(
            self,
            root_path,
            glob,
            polling_interval=1,
            stability_threshold=1,
    ):
        self._root_path = root_path
        self._glob = glob
        self._polling_interval = polling_interval
        self._stability_threshold = stability_threshold
        self._snapshot = None

    def _make_snapshot(self) -> SnapShot:
        return SnapShot(
            root_path=self._root_path,
            glob=self._glob,
            stability_threshold=self._stability_threshold)
    def take_snapshot(self):
        if not self._snapshot:
            self._snapshot = self._make_snapshot()
        else:
            self._snapshot = self._snapshot.next()

    def iter_events(self):
        while True:
            self.take_snapshot()
            for event in self._snapshot.iter_events():
                yield event
