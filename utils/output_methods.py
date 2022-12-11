White = '\033[0m'
Bold = '\033[1m'
Red = '\033[31m'
Green = '\033[32m'
Blue = '\033[34m'


def print_error(text: str):
    print(f"[{Bold}{Red}!{White}] {text}")


def print_success(text: str):
    print(f"[{Bold}{Green}+{White}] {text}")


def print_info(text: str):
    print(f"[{Bold}{Blue}*{White}] {text}")


def print_banner():
    print(f"""
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
          
          Written by @flashnuke
          """)
