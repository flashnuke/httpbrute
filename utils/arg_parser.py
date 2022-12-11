import argparse


def get_argument_parser() -> argparse.ArgumentParser:
    # Create the parser and add arguments
    parser = argparse.ArgumentParser(description=f'A tool for brute-forcing HTTP auth login pages',
                                     formatter_class=argparse.RawTextHelpFormatter,
                                     usage=f"./httpbrute <url> -u <username> -P <passwords.lt>",
                                     epilog="This tool supports two types of HTTP authentication:"
                                            "* BasicAuth"
                                            "* DigestAuth")

    parser.add_argument(dest='target_url', type=str, help="url of targeted login page")

    parser.add_argument("-u", "--user", dest='user', action='store', type=str, default=str(),
                        help="username (single)")

    parser.add_argument("-U", "--user-list", dest='user_list', action='store', type=str, default=str(),
                        help="path to a username list (multiple)")

    parser.add_argument("-p", "--pass", dest='pass', action="store", default=str(),
                        type=str, help="password (single)")

    parser.add_argument("-P", "--pass-list", dest='pass_list', action="store", default=str(),
                        type=str, help="path to a password list (multiple)")

    parser.add_argument("-w", "--workers", dest='workers', action="store", type=int,
                        default=16, help="number of workers / threads (default -> 16)")

    parser.add_argument("-t", f"--timeout", dest='timeout', action="store",
                        type=int, default=10, help='request timeout (default -> 10)')

    parser.add_argument("-s", f"--sleep", dest='sleep', action="store",
                        type=float, default=0.0, help='sleep interval between request for each worker (default -> 0)')

    return parser
