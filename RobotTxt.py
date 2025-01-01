#!/usr/bin/python3
import argparse
import requests
from urllib.parse import urljoin
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def fetch_and_parse_robots(domain, follow_redirects=False, status_filter=None, show_status=True, silent=False):
    """
    Fetch robots.txt from the given domain, parse Disallow/Allow paths,
    and construct potential URLs while excluding main domain and '*'.
    """
    subdomains = {}
    fetched = set()  # To prevent duplicate fetching of robots.txt
    protocols = ["https://", "http://"]

    # Ensure domain starts with a protocol if not present
    if not any(domain.startswith(protocol) for protocol in protocols):
        domain = "https://" + domain

    for protocol in protocols:
        try:
            url = urljoin(domain, "/robots.txt")  # Construct robots.txt URL using the base domain
            if url in fetched:  # Skip already fetched robots.txt
                continue
            fetched.add(url)
            response = requests.get(url, timeout=10, allow_redirects=follow_redirects)

            if response.status_code == 200:
                if not silent:
                    print(f"{Fore.GREEN}[+] robots.txt found for {domain}")
                subdomains.update(parse_robots_paths(response.text, domain, follow_redirects, status_filter, show_status, silent))
                break  # Stop scanning after successful robots.txt fetch
        except requests.RequestException:
            pass  # Silently handle errors

    return subdomains

def parse_robots_paths(content, base_url, follow_redirects, status_filter, show_status, silent):
    """
    Parse the Disallow and Allow paths from robots.txt content
    and construct full URLs based on the base domain while excluding main domain and '*'.
    """
    paths = {}
    for line in content.splitlines():
        line = line.strip()
        if line.startswith(("Disallow:", "Allow:")):
            path = line.split(":", 1)[1].strip()
            if path and "*" not in path:
                full_url = urljoin(base_url, path)
                status = get_status(full_url, follow_redirects)
                if status_filter is None or (isinstance(status, int) and status in status_filter):
                    paths[full_url] = status
    return paths

def get_status(url, follow_redirects):
    """
    Get the HTTP status code of a URL.
    """
    try:
        response = requests.head(url, timeout=10, allow_redirects=follow_redirects)
        return response.status_code
    except requests.RequestException:
        return "Error"

def print_results(subdomains, show_status):
    """
    Print the collected subdomains with their status codes in color.
    """
    if subdomains:
        print("\n[+] Subdomain-like URLs found:")
        for url, status in subdomains.items():
            url_clickable = f"\033]8;;{url}\033\\{url}\033]8;;\033\\"
            if show_status:
                if isinstance(status, int) and 200 <= status < 300:
                    print(f"{Fore.GREEN}{url_clickable} - Status: {status}")
                elif isinstance(status, int) and 300 <= status < 400:
                    print(f"{Fore.YELLOW}{url_clickable} - Status: {status} (Redirect)")
                elif isinstance(status, int):
                    print(f"{Fore.RED}{url_clickable} - Status: {status}")
                else:
                    print(f"{Fore.RED}{url_clickable} - Status: {status}")
            else:
                print(f"{url_clickable}")

def process_single_domain(domain, follow_redirects, status_filter, show_status, silent):
    """
    Process a single domain for robots.txt and extract paths as subdomain-like URLs.
    """
    if not silent:
        print(f"[*] Processing domain: {domain}")
    subdomains = fetch_and_parse_robots(domain, follow_redirects, status_filter, show_status, silent)
    if subdomains:  # Only print results if subdomains are found
        print_results(subdomains, show_status)

def process_domain_list(file_path, follow_redirects, status_filter, show_status, silent):
    """
    Process a list of domains for robots.txt and extract paths as subdomain-like URLs.
    """
    if not silent:
        print(f"[*] Processing domain list from: {file_path}")
    try:
        with open(file_path, 'r') as file:
            domains = [line.strip() for line in file if line.strip()]

        all_subdomains = {}
        for domain in domains:
            subdomains = fetch_and_parse_robots(domain, follow_redirects, status_filter, show_status, silent)
            if subdomains:  # Only add if subdomains are found
                all_subdomains.update(subdomains)

        if all_subdomains and not silent:
            print_results(all_subdomains, show_status)
    except FileNotFoundError:
        if not silent:
            print(f"{Fore.RED}[-] File not found: {file_path}")
    except Exception as e:
        if not silent:
            print(f"{Fore.RED}[-] An error occurred while processing the file: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Fetch robots.txt and extract Disallow/Allow paths as URLs.",
        epilog="Example usage:\n  python3 robots_paths.py -u example.com\n  python3 robots_paths.py -dl domains.txt -r",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--url", help="Single domain to check for robots.txt.")
    parser.add_argument("-dl", "--domainlist", help="File containing a list of domains.")
    parser.add_argument("-r", "--redirect", action="store_true", help="Follow redirects while checking URLs.")
    parser.add_argument("-mc", "--matchcodes", nargs='+', type=int, help="Filter results by specific status codes (e.g., 200, 301).")
    parser.add_argument("-ns", "--nostatus", action="store_true", help="Do not show status codes in the output.")
    parser.add_argument("--silent", action="store_true", help="Silent mode: no output shown.")
    args = parser.parse_args()

    status_filter = set(args.matchcodes) if args.matchcodes else None
    show_status = not args.nostatus

    if args.url:
        process_single_domain(args.url, args.redirect, status_filter, show_status, args.silent)
    elif args.domainlist:
        process_domain_list(args.domainlist, args.redirect, status_filter, show_status, args.silent)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
