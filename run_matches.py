"""
This module runs matches between two of our bots.

If an error occurred, it dumps the information to disk
so we can debug it.
"""

import os
import sys
import time

from subprocess import Popen, STDOUT, TimeoutExpired


TOTAL_MATCHES = 2

DATA_ZIP_PATH = sys.argv[1]

LOG_PATH = "match_results"

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

cmd_server = [os.path.join(DATA_ZIP_PATH, "server/server"),
              "10000"]

cmd_client = [os.path.join(DATA_ZIP_PATH, "client/client"),
              "0.0.0.0", "10000", "--noBoard", "main.py"]


def wait_for(*args, timeout=15):
    for proc in args:
        try:
            proc.wait(timeout=timeout)
        except TimeoutExpired:
            # print("Process timed out: %r" % proc.args[0])
            pass


def killall(*args, timeout=15):
    for proc in args:
        proc.kill()


def log_files(match_count):
    return [
        open(os.path.join(LOG_PATH,  "%d_%s.log" % (match_count, filename)), mode="w")
        for filename in ["server", "p1", "p2"]
    ]


def rm_files(*args):
    for file in args:
        os.remove(file.name)


match_count = 0
while match_count < TOTAL_MATCHES:

    match_count += 1

    print("Running Match %d" % match_count)

    # Run 3 processes
    s_log, p1_log, p2_log = log_files(match_count)

    s = Popen(cmd_server,  stdout=s_log,  stderr=STDOUT)
    p1 = Popen(cmd_client, stdout=p1_log, stderr=STDOUT)
    p2 = Popen(cmd_client, stdout=p2_log, stderr=STDOUT)

    # Wait for them to finish
    wait_for(s, p1, p2, timeout=15)
    killall(s, p1, p2)

    # Open the file again
    with open(s_log.name, "r") as s_log:
        contents = s_log.read()

    # If everythin was ok, then delete these logs!
    if "'action': 'FINISH'" in contents:
        rm_files(s_log, p1_log, p2_log)

        print("    Ok")

        # TODO: Extract which player won?
    else:
        print("    Error!")

    time.sleep(15)
