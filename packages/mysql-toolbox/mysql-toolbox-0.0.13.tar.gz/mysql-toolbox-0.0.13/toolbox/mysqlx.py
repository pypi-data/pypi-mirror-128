#!/usr/bin/python3

import sys
import os
import re
from xtable import xtable
import xmltodict
import argparse
import json
import traceback

mysqlcmds = dict()
mysqlcmds["show databases"] = "select * from information_schema.schemata"
mysqlcmds["show tables"] = "select table_schema, table_name, table_type type, engine, table_rows, avg_row_length, data_length, coalesce(update_time,create_time) last_change, check_time last_chk from information_schema.tables where database() is NULL or table_schema = database()"



def mysqlx_main():
    parser = argparse.ArgumentParser(description="yet another mysql client CLI tool/shell")
    parser.add_argument(
        "-v",
        "--pivot",
        dest="pivot",
        action="store_true",
        default=False,
        help="pivot wide tables.",
    )
    parser.add_argument(
        "-w",
        "--widthhint",
        dest="widthhint",
        default=None,
        help="hint for col width. '0:20,2:30,'",
    )
    parser.add_argument(
        "-p",
        "--page",
        dest="page",
        type=int,
        default=2**30,
        help="rows per page. print header line again",
    )
    parser.add_argument(
        "-X",
        "--debug",
        dest="debug",
        action="store_true",
        default=False,
        help="debug mode",
    )
    parser.add_argument(
        "--csv",
        dest="csv",
        action="store_true",
        default=False,
        help="dump as CSV",
    )
    parser.add_argument(
        "--json",
        dest="json",
        action="store_true",
        default=False,
        help="dump as json",
    )
    parser.add_argument(
        "--yaml",
        dest="yaml",
        action="store_true",
        default=False,
        help="dump as yaml",
    )
    parser.add_argument(
        "--markdown",
        dest="markdown",
        action="store_true",
        default=False,
        help="dump as markdown",
    )
    parser.add_argument(
        "--html",
        dest="html",
        action="store_true",
        default=False,
        help="dump as html",
    )
    parser.add_argument(
        "--plain",
        "--nocolor",
        dest="plain",
        action="store_true",
        default=False,
        help="no ansi color",
    )
    parser.add_argument(
        "--nowrap",
        "--nowrap",
        dest="nowrap",
        action="store_true",
        default=False,
        help="when specified, output will be limited to current terminal width",
    )
    parser.add_argument(
        "--wrap",
        "--wrap",
        dest="wrap",
        action="store_true",
        default=False,
        help="wrap mode. widthhint will be disabled in this mode.",
    )
    parser.add_argument(
        "--timeout",
        dest="timeout",
        type=int,
        default=1,
        help="read timeout. default 1s",
    )
    args = parser.parse_args()

    if args.plain:
        os.environ["force_ansicolor"] = "0"

    def xtimeout_call(fn=None, msg="timeouted.",exitfn=None) :
        import signal
        TIMEOUT = 1
        def interrupted(signal, frame):
            print("# {}".format(msg), file=sys.stderr, flush=True)
            if exitfn :
                exitfn()
            sys.exit(-1)
        signal.signal(signal.SIGALRM, interrupted)
        signal.alarm(TIMEOUT)
        res = None
        if fn :
            res = fn()
        signal.alarm(0)
        return res
    xinput = xtimeout_call(sys.stdin.read, "Timeout getting input from STDIN.", parser.print_help)
    xinput = xinput.strip()
    if not (xinput.lower().startswith("select") \
      or xinput.lower().startswith("update") \
      or xinput.lower().startswith("insert") \
      or xinput.lower().startswith("delete") \
      or xinput.lower().startswith("with") ) :
          k = re.sub(r"\s+"," ",xinput.lower())
          if k in mysqlcmds :
              xinput = mysqlcmds[k]
          else :
              xinput = None
    print(xinput)



if __name__ == "__main__":
    mysqlx_main()
