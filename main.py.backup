#=============================================================================#
#                              Python Project                                 #
#       SI 100B: Introduction to Information Science and Technology           #
#                       Fall 2020, ShanghaiTech University                    #
#                     Author: Diao Zihao <hi@ericdiao.com>                    #
#                         Last motified: 07/07/2020                           #
#=============================================================================#

# NOTE to student:
# YOU ARE NOT SUPPOSED TO EDIT THE FILE.
#
# This file is intended to provide a unified entrypoint for your web server
# and the cralwer. You can treat this file as a black box. Being unable to
# know how the magic in this file works won't cause trouble to you finishing
# the project. If you feel the need to edit it, do it at your own risk.
# Understand every line of the file before proceed to editing. When in doubt,
# ask on Piazza.

from state import State
from data_source.fr24_crawler import Fr24Crawler
from web_server.server import web_server
from cli.cli import cli_start
import os
import sys
import logging


def _help():
    print("Usage:")
    print()
    print("  {} --web | --cli".format(sys.argv[0]))
    print()
    print("If you choose to implement the CLI (easy level), run:")
    print()
    print("  {} --cli".format(sys.argv[0]))
    print()
    print("If you choose to implement the web server (advanced level), run:")
    print()
    print("  {} --web".format(sys.argv[0]))
    print()


if __name__ == "__main__":
    logger = logging.getLogger("si100b_proj:main")
    logger.setLevel("INFO")

    if len(sys.argv) != 2:
        logger.error("Except 1 argument, get {}.".format(len(sys.argv)-1))
        _help()
        exit(-1)
    if not (sys.argv[1] == "--web" or sys.argv[1] == "--cli"):
        logger.error("Invalid argument.")
        _help()
        exit(-1)
    else:
        flag = sys.argv[1]

    # Create a new process.
    # `fork()` is a UNIX syscall that creates a new process.
    # `os.fork` is a Python wrapper of it. See `man fork` for more information.
    pid = os.fork()
    if (pid == 0):
        # The child process.
        # In this process, we run the web server / cli.
        ppid = os.getppid()
        try:
            if flag == '--web':
                web_server.run(host="0.0.0.0", port=9000)
            elif flag == '--cli':
                cli_start()
        except KeyboardInterrupt:
            logger.warning("Control panel exits.")
            os.kill(ppid)
    else:
        # The parent process.
        # In this process, we run the cralwer.
        cralwer_pid = os.fork()
        if cralwer_pid == 0:
            ppid = os.getppid()
            try:
                state = State()
                state.spin()
            except KeyboardInterrupt:
                os.kill(ppid)
        else:
            try:
                cralwer = Fr24Crawler((0, 0), 0)
                cralwer.spin()
            except KeyboardInterrupt:
                # The process is being killed, let the child process exit.
                logger.warning("Crawler exits.")
                os.kill(pid)
                os.kill(cralwer_pid)
