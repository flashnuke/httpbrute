White = '\033[0m'
Bold = '\033[1m'
Red = '\033[31m'
Green = '\033[32m'
Blue = '\033[34m'
Gray = '\033[37m'

DELIMITER = f"{Gray}=========================================={White}"
BANNER = f"""
{Red}██╗  ██╗{White}████████╗{Red}████████╗{White}██████╗         
{Red}██║  ██║{White}╚══██╔══╝{Red}╚══██╔══╝{White}██╔══██╗        
{Red}███████║{White}   ██║   {Red}   ██║   {White}██████╔╝        
{Red}██╔══██║{White}   ██║   {Red}   ██║   {White}██╔═══╝         
{Red}██║  ██║{White}   ██║   {Red}   ██║   {White}██║             
{Red}╚═╝  ╚═╝{White}   ╚═╝   {Red}   ╚═╝   {White}╚═╝             

{Red}██████╗ {White}██████╗ {Red}██╗   ██╗{White}████████╗{Red}███████╗{White}
{Red}██╔══██╗{White}██╔══██╗{Red}██║   ██║{White}╚══██╔══╝{Red}██╔════╝{White}
{Red}██████╔╝{White}██████╔╝{Red}██║   ██║{White}   ██║   {Red}█████╗  {White}
{Red}██╔══██╗{White}██╔══██╗{Red}██║   ██║{White}   ██║   {Red}██╔══╝  {White}
{Red}██████╔╝{White}██║  ██║{Red}╚██████╔╝{White}   ██║   {Red}███████╗{White}
{Red}╚═════╝ {White}╚═╝  ╚═╝{Red} ╚═════╝ {White}   ╚═╝   {Red}╚══════╝{White}
{DELIMITER}
Written by {Bold}{Red}@flashnuke{White}
{DELIMITER}
"""


def print_error(text: str):
    print(f"[{Bold}{Red}!{White}] {text}")


def print_success(text: str):
    print(f"[{Bold}{Green}+{White}] {text}")


def print_fail(text: str):
    print(f"[{Bold}{Red}-{White}] {text}")


def print_info(text: str, reset_line=False):
    text = f"[{Bold}{Blue}*{White}] {text}"
    if reset_line:
        print(text, end="\r")
    else:
        print(text)


def print_banner():
    print(BANNER)
