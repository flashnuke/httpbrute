import argparse

_DEF_WORKERS = 16
_DEF_TIMEOUT = 10
_DEF_SLEEP = 0.0


def get_argument_parser() -> argparse.ArgumentParser:
    # Create the parser and add arguments
    parser = argparse.ArgumentParser(description=f'A tool for brute-forcing HTTP auth login pages',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     usage=f"./httpbrute.py <url> -u <username> -P <passwords.lt>",
                                     epilog="This tool supports two types of HTTP authentication:"
                                            "* BasicAuth"
                                            "* DigestAuth")

    parser.add_argument(dest="target_url", type=str, help="url of targeted login page")

    parser.add_argument("-u", "--user", dest='user', action='store', type=str, default=str(),
                        metavar="<username>", help="username (single)")

    parser.add_argument("-U", "--user-list", dest='user_list', action='store', type=str, default=str(),
                        metavar="<path>", help="path to username list (multiple)")

    parser.add_argument("-p", "--pass", dest='pass', action="store", default=str(),
                        metavar="<password>", type=str, help="password (single)")

    parser.add_argument("-P", "--pass-list", dest='pass_list', action="store", default=str(),
                        metavar="<path>", type=str, help="path to password list (multiple)")

    parser.add_argument("-w", "--workers", dest='workers', action="store", type=int,
                        metavar="<count>", default=_DEF_WORKERS, help=f"number of workers / threads "
                                                                      f"(default -> {_DEF_WORKERS})")

    parser.add_argument("-t", "--timeout", dest='timeout', action="store",
                        metavar="<time>", type=int, default=_DEF_TIMEOUT,
                        help=f"request timeout (default -> {_DEF_TIMEOUT})")

    parser.add_argument("-s", "--sleep", dest='sleep', action="store", metavar="<seconds>",
                        type=float, default=_DEF_SLEEP, help=f"sleep interval between request for each worker "
                                                             f"(default -> {_DEF_SLEEP})")

    return parser
