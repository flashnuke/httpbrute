![image](https://user-images.githubusercontent.com/59119926/207055888-c8cc35d6-0f2a-4bd2-a8db-256287488649.png)

Crack HTTP authentication by brute-force

Types of authentication currently supported:
* Basic Auth
* Digest Auth


# Requirements
Works on every OS. </br>
Regarding 3rd party libraries, only `requests` is required and could be installed by running the following command from the project's directory:
> pip3 install -r requirements.txt

# Usage
The basic usage where one username is tested against a list of passwords is very straightforward
```bash
./httpbrute <taret_url> -u <username> -P <path_to_passlist>
```

### Notes
* Brute-forcing multiple users is possible by passing `-U <path_to_userlist>` instead of `-u <username>`
* It is possible to test a single password by passing `-p <password>` instead of `-P <path_to_passlist>`</br>
(useful for cases where only the username is known)
### Optional params
| param | description | default |
|---|---|---|
| -s, --sleep | sleep between requests (each worker individually) | 0[s] |
| -t, --timeout | request timeout in seconds | 10[s] |
| -w. --workers | amount of workers (running threads) | 16 |

# Disclaimer

This tool is only for testing and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. I assume no liability and am not responsible for any misuse or damage caused by this tool and software.

Distributed under the GNU License.
