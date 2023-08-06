from qsync import SyncIniter
from multiprocessing import freeze_support
import argparse
from qsync import server
from requests import get
from requests.exceptions import ConnectTimeout


def main():

    # nothing usefull, just parsing command line args

    parser = argparse.ArgumentParser(description="")

    parser.add_argument('sync_src', type=str,
                        help='sync source directory')

    parser.add_argument('sync_dst', type=str,
                        help='sync destination directory')

    parser.add_argument('-bd', action='store_true',
                        help='bi directionnal mode')

    parser.add_argument('--force-id', type=str,
                        help='force a specific id associated to the sync process (necessary to acces via http)')

    parser.add_argument('--remote', type=str,
                        help='open sync server, specify destination ip')

    parser.add_argument('--loop-time', type=float,
                        help='adjust the time between two sync (each use has it\'s own optimal inter-loop time to avoid sync errors)')

    args = parser.parse_args()

    sync_src = args.sync_src.replace("\\", "/")
    sync_dst = args.sync_dst.replace("\\", "/")
    bi_d = args.bd
    if args.remote is not None:
        remote_ip = args.remote
        remote = True
    else:
        remote_ip = ""
        remote = False

    force_id = args.force_id
    loop_time = args.loop_time if args.loop_time is not None else 0.5

    # sync_src and sync_dst must be two strings containing two path
    # bi_directionnal is an optionnal boolean, default set to False
    # remote is an optionnal boolean, set to True if the sync_dst path is on a remote location
    # force_id let you specify the sync id, usefull in case of remote and/or want to keep a sync state after shutdown
    # loop_time let you adjust the time between two sync (each use has it\'s own optimal inter-loop time to avoid sync errors)
    s = SyncIniter(sync_src, sync_dst, bi_directionnal=bi_d,
                   remote=remote, force_id=force_id, remote_ip=remote_ip, loop_time=loop_time)
    s.start_sync()

    print(f"\n\nSYNC ID :\n{s.sync_id}\n\n")

    # start the server if the other side is on a remote machine if not already running
    if remote:
        try:
            get("https://127.0.0.1:2121/is_running", timeout=1, verify=False)
        except ConnectTimeout:
            server.app.run(host="0.0.0.0", port=2121,
                           ssl_context='adhoc')


if __name__ == "__main__":

    freeze_support()

    main()
