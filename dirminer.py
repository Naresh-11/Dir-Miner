import argparse
import requests
from colorama import Fore, Style, init, Back
import pyfiglet
import sys
import random

init(autoreset=True)

def load_wordlist(wordlist_file):
    try:
        with open(wordlist_file, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"{random.choice([Fore.RED, Fore.MAGENTA])}Wordlist file '{wordlist_file}' not found.{Style.RESET_ALL}")
        return []
    except Exception as e:
        print(f"{random.choice([Fore.RED, Fore.MAGENTA])}An error occurred while loading the wordlist: {e}{Style.RESET_ALL}")
        return []

def print_colored(text, text_color=None, bg_color=None, style=Style.RESET_ALL):
    if text_color is None:
        text_color = random.choice([Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN])
    if bg_color is None:
        bg_color = random.choice([Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN])
    
    formatted_text = f"{bg_color}{text_color}{style}{text}{Style.RESET_ALL}"
    print(formatted_text)

def print_welcome_message():
    welcome_text = pyfiglet.figlet_format("FUZZER", font="block")
    print_colored(welcome_text, Fore.BLUE, bg_color=random.choice([Back.BLACK, Back.WHITE]))
    print_colored("A simple dir-miner tool developed by Mr. ND", Fore.GREEN)
    print("\n" * 2)

def print_farewell_message(author_name):
    print("\n" * 2)
    print_colored("Thanks for using this tool!", Fore.YELLOW)
    print_colored(f"Author: {author_name}", Fore.CYAN)

def save_to_file(output_file, text):
    try:
        with open(output_file, 'a') as file:
            file.write(text + '\n')
    except Exception as e:
        print(f"An error occurred while saving to the output file: {e}")

def dirsearch(target_url, wordlist, timeout, user_agent, follow_redirects, verbose, output_file=None):
    try:
        session = requests.Session()
        session.headers['User-Agent'] = user_agent

        for directory in wordlist:
            url = f"{target_url}/{directory}"
            response = session.get(url, timeout=timeout, allow_redirects=follow_redirects)

            status_code_color = Fore.GREEN if response.status_code == 200 else Fore.RED
            result = f"{url} ({response.status_code})"
            print_colored(result, status_code_color)

            if output_file:
                save_to_file(output_file, result)

    except requests.RequestException as e:
        if verbose:
            print_colored(f"Request error: {e}", Fore.RED)
    except KeyboardInterrupt:
        print_colored("Fuzzing interrupted by user.", Fore.YELLOW)
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
    parser.add_argument("-o", "--output", help="Output file to save results.")

    args = parser.parse_args()

    print_welcome_message()

    if args.wordlist is None:
        wordlist = load_wordlist("wordlist.txt")
    else:
        wordlist = load_wordlist(args.wordlist)
    
    dirsearch(args.url, wordlist, args.timeout, args.user_agent, args.follow_redirects, args.verbose, args.output)

    print_farewell_message("Mr. ND")

    sys.exit(0)
