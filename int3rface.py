import sys
import argparse
import json
import requests
import socket
import os
from termcolor import colored

from code.enumerate_subdomains import return_subdomains
from code.detect_login import detect_login
from code.crawl_site import crawl_site
from code.check_alive import check_alive


def parse_infile(infile):
    try:
        with open(infile, 'r', encoding="ISO-8859-1") as file:
            parsed = [i.replace('https://', '')
                      for i in [j.strip() for j in file.readlines()]]
            return parsed
    except Exception as e:
        print(colored(f'\n [ERROR] Invalid input file', 'red'))
        exit()


def main(args, domain):
    print(
        f"\n\n[INFO] Gathering subdomains from crt.sh for {colored(domain,'blue')}")
    subdomains = return_subdomains(domain.lower())
    if len(subdomains) == 0:
        print(
            colored(f'\n[ERROR] No alive subdomains were found in crt.sh\'s database.\n', 'red'))
        exit()

    # Quick check to return subdomains that are alive
    subdomains = check_alive(domain.lower(), subdomains)

    # Start the login detection
    print(f"    [*] Found {len(subdomains)} subdomains\n")
    results = detect_login(subdomains, args.timeout,
                           args.screenshot, args.open)

    # If crawl flag was set, begin crawl function for each returned subdomain
    if args.crawl == True:
        print(
            f'\n[INFO] Crawling subdomains for internal links to check for login forms\n')
        for subdomain in subdomains:
            internal_links = crawl_site(subdomain, args.timeout)
            if internal_links:
                internal_links = list(set(internal_links))
                print(
                    f"    [*] Found {len(internal_links)} internal link[s] on {colored(subdomain,'blue')}, checking for login portals...\n")
                detect_login(internal_links, args.timeout, args.screenshot)

    # If outfile flag was set, write results to file
    if args.outfile != None:
        try:
            with open(args.outfile, 'a') as file:
                for result in results['results']:
                    if result['pub_login'] == True:
                        file.write(result['subdomain']+'\n')

        except Exception as e:
            print(f"There was an error writing to the file")
            exit()


if __name__ == "__main__":
    if not os.path.isdir('screenshots'):
        os.makedirs('screenshots')

    parser = argparse.ArgumentParser(
        prog='Int3rface',
        description='A script to detect publicly facing login portals on websites.',
        epilog='Developed by github.com/BDragisic')

    parser.add_argument(
        '-d', '--domain', help='Specify a single domain to scan'
    )

    parser.add_argument(
        '-s', '--screenshot', help="Take screenshots of all login portals discovered", action="store_true")
    parser.add_argument(
        '-x', '--open', help='Open all matches in browser', action='store_true'
    )
    parser.add_argument('-t', '--timeout', default=5,
                        help="Specifiy how long in seconds to wait for a page to load, defaults to 5 seconds.")
    parser.add_argument('-o', '--outfile',
                        help='\nSpecify the path to output file.')
    parser.add_argument('-i', '--infile',
                        help='\nSpecify a file containing a list of domains list (newline separated).')
    parser.add_argument(
        '-c', '--crawl', help='\nNon-recursively crawl every subdomain to find potential directories with login portals', action='store_true')

    args = parser.parse_args()

    print('''
_______________________________________________________
 _____         _    _____         __                    
|_   _|       | |  |____ |       / _|                   
  | |   _ __  | |_     / / _ __ | |_   __ _   ___   ___ 
  | |  | '_ \ | __|    \ \| '__||  _| / _` | / __| / _\\
 _| |_ | | | || |_ ____/ /| |   | |  | (_| || (__ |  __/
 \___/ |_| |_| \__|\____/ |_|   |_|   \__,_| \___| \___|    
 
[*] Developed by github.com/BDragisic
_______________________________________________________
 
                                    
          ''')

    if args.infile != None:
        domains = parse_infile(args.infile)

        for domain in domains:
            main(args, domain)

    else:
        main(args, args.domain)
