#!/usr/bin/python3

import sys
import os
import re
from xtable import xtable
import xmltodict
import argparse
import json
import traceback


def xml_formatter_main():
    parser = argparse.ArgumentParser(description="format 'mysql --xml' output")
    parser.add_argument(
        "-I",
        "--includes",
        dest="includes",
        default=list(),
        action="append",
        help="when defined only include column names match RE.",
    )
    parser.add_argument(
        "-E",
        "--excludes",
        dest="excludes",
        default=list(),
        action="append",
        help="when defined exclude column names match RE.",
    )
    parser.add_argument(
        "-R",
        "--preprocessing",
        "--replacements",
        dest="preprocessing",
        default=list(),
        action="append",
        help=
        "to mask/modify field values before processing. useful when need masking or some special characters in column such as authentication_string may break the following processing. in format of 'field=xxx,field2=xxx2'",
    )
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
        "--cutwrap",
        "--cutwrap",
        dest="cutwrap",
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

    import signal
    TIMEOUT = 1

    def interrupted(signal, frame):
        print("# timeout/no input from STDIN detected.",
              file=sys.stderr,
              flush=True)
        parser.print_help()
        sys.exit(0)

    signal.signal(signal.SIGALRM, interrupted)
    signal.alarm(TIMEOUT)
    xmlinput = sys.stdin.read()
    signal.alarm(0)

    if len(args.preprocessing) > 0:
        pairs = dict()
        for pre in args.preprocessing:
            for p in [p for p in pre.split(",") if p and '=' in p]:
                field, value = p.split('=', 1)
                if field:
                    pairs[field] = value or ""
        newxml = xmlinput
        for field, value in pairs.items():
            newxml = re.sub(
                r"<field name=\"{}\">.*?</field>".format(field),
                "<field name=\"{}\">{}</field>".format(field, value), newxml,
                re.DOTALL)
        xmlinput = newxml

    try:
        doc = xmltodict.parse(xmlinput)
    except:
        xmldata = [str(lno) + " : " + ln for lno, ln in enumerate(xmlinput.splitlines())]
        errmsg = traceback.format_exc().splitlines()[-1]
        m = re.search(r"not well-formed \(invalid token\): line (\d+),",errmsg) 
        if m :
            lno = int(m.group(1))
            begin = max(lno-3,0)
            end = lno+4
            print("\n".join(xmldata[begin:end]),file=sys.stderr,flush=True)
        else :
            print("{}".format("\n".join(xmldata)), file=sys.stderr, flush=True)
        print("# error parsing XML contents : {}".format(errmsg), file=sys.stderr, flush=True)
        return -1
    if "resultset" not in doc:
        print("# not valid resultset XML contents :",
              file=sys.stderr,
              flush=True)
        print(xmlinput, file=sys.stderr, flush=True)
        return -1

    rs = doc["resultset"]
    if args.debug:
        print("# resultset section : \n",
              json.dumps(rs, indent=2),
              file=sys.stderr,
              flush=True)
    if "row" not in rs or len(rs["row"]) == 0:
        print("# found no data :", file=sys.stderr, flush=True)
        return -1

    rows = rs["row"]
    if type(rows) is not list:
        rows = [rows]
    tbl = list()
    for r in rows:
        if args.debug:
            print("# row :", r, file=sys.stderr, flush=True)
        t = {}
        e = r.get("field", [])
        if type(e) is not list:
            e = [e]
        for c in e:
            if len(args.includes) > 0:
                found = False
                for sect in args.includes:
                    for inx in [s for s in sect.split(",") if s]:
                        if re.search(r"{}".format(inx), c.get('@name'),
                                     re.IGNORECASE):
                            found = True
                            break
                if not found:
                    continue
            if len(args.excludes) > 0:
                found = False
                for sect in args.excludes:
                    for ex in [s for s in sect.split(",") if s]:
                        if re.search(r"{}".format(ex), c.get('@name'),
                                     re.IGNORECASE):
                            found = True
                            break
                if found:
                    continue
            t[c.get('@name')] = c.get('#text')
        tbl.append(t)

    if args.debug:
        print("# table data prepared :\n",
              json.dumps(tbl, indent=2),
              file=sys.stderr,
              flush=True)

    if len(tbl) == 0:
        print("# empty result set.", file=sys.stderr, flush=True)
        return 0

    xt = xtable.init_from_list(tbl)
    if args.widthhint or args.page != 2**30 or args.wrap or args.cutwrap :
        xt = xtable(data=xt.get_data(),
                    header=xt.get_header(),
                    widthhint=args.widthhint,
                    superwrap=args.wrap,
                    cutwrap=args.cutwrap,
                    debug=args.debug,
                    rowperpage=args.page)
    if args.pivot:
        print(xt.pivot())
    elif args.csv:
        print(xt.csv())
    elif args.json:
        print(xt.json())
    elif args.yaml:
        print(xt.yaml())
    elif args.markdown:
        print(xt.markdown())
    elif args.html:
        print(xt.html())
    else:
        print(xt)


if __name__ == "__main__":
    xml_formatter_main()
