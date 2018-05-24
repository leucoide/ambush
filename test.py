from time import sleep

from memory_profiler import profile

from ambush.snapshot import SnapShot


@profile
def main():

    try:
        snapshot = SnapShot(
            root_path='.',
            glob='**/*.py',
            stability_threshold=10,
        )

        while True:
            sleep(1)
            snapshot = snapshot.next()
            for event in snapshot.iter_events():
                print('[{event_type}] {path}'.format(**event))
    except KeyboardInterrupt:
        return


main()
