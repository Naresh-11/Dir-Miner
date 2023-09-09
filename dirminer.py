import argparse
import requests
from colorama import Fore, Back, Style, init
import pyfiglet
import sys


init(autoreset=True)


def load_wordlist(wordlist_file):
    try:
        with open(wordlist_file, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}Wordlist file '{wordlist_file}' not found.{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{Fore.RED}An error occurred while loading the wordlist: {e}{Style.RESET_ALL}")
        return []


def print_colored(text, text_color=Fore.RESET, bg_color=Back.RESET, style=Style.RESET_ALL):
    formatted_text = f"{bg_color}{text_color}{style}{text}{Style.RESET_ALL}"
    print(formatted_text, end="")

def print_welcome_message():
    welcome_text = pyfiglet.figlet_format("FUZZER", font="block")
    print_colored(welcome_text, Fore.BLUE)
    print_colored("A simple directory search tool developed by Mr. ND", Fore.GREEN)
    print("\n" * 2)  

def print_farewell_message(author_name):
    print("\n" * 2) 
    print_colored("Thanks for using this tool!", Fore.YELLOW)
    print_colored(f"Author: {author_name}", Fore.CYAN)

def dirsearch(target_url, wordlist, timeout, user_agent, follow_redirects, verbose):
    try:
        session = requests.Session()
        session.headers['User-Agent'] = user_agent

        for directory in wordlist:
            url = f"{target_url}/{directory}"
            response = session.get(url, timeout=timeout, allow_redirects=follow_redirects)

            if response.status_code == 200:
                print_colored(f"Found: {url} ({response.status_code})", Fore.GREEN)
                if verbose:
                    print_colored(response.text, Fore.BLUE)
            elif response.status_code == 403:
                print_colored(f"Forbidden: {url} ({response.status_code})", Fore.YELLOW)
            elif response.status_code == 404:
                print_colored(f"Not Found: {url} ({response.status_code})", Fore.RED)
            
            sys.stdout.write("\033[F")  
            sys.stdout.write("\033[F")  
            sys.stdout.write("\033[K")  

    except requests.RequestException as e:
        if verbose:
            print_colored(f"Request error: {e}", Fore.RED)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple directory search tool.")
    parser.add_argument("-u", "--url", required=True, help="Target URL to search.")
    parser.add_argument("-w", "--wordlist", help="Wordlist file containing directories to check.")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, help="Timeout for HTTP requests (default: 5.0 seconds)")
    parser.add_argument("-ua", "--user-agent", default="DirectorySearchBot", help="Custom User-Agent header for HTTP requests")
    parser.add_argument("-f", "--follow-redirects", action="store_true", help="Follow HTTP redirects")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")

    args = parser.parse_args()

    print_welcome_message() 

    if args.wordlist is None:
        wordlist = load_wordlist("wordlist.txt") 
    else:
        wordlist = load_wordlist(args.wordlist)  
    
    dirsearch(args.url, wordlist, args.timeout, args.user_agent, args.follow_redirects, args.verbose)

   
    print_farewell_message("Mr. ND")

    sys.exit(0)  