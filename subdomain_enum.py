import dns.resolver
import requests
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, Style
import argparse
import os
import signal
import threading

# Stop event for graceful exit
stop_event = threading.Event()

def signal_handler(sig, frame):
    print("\n[!] Exiting gracefully...")
    stop_event.set()

signal.signal(signal.SIGINT, signal_handler)

# Function to resolve and check subdomains
def check_subdomain(domain, subdomain, output_file):
    if stop_event.is_set():
        return

    full_domain = f"{subdomain}.{domain}"
    try:
        # DNS resolution
        dns.resolver.resolve(full_domain, 'A')
        print(f"{Fore.GREEN}[+] DNS Found: {full_domain}{Style.RESET_ALL}")

        # HTTP check
        try:
            response = requests.get(f"http://{full_domain}", timeout=3)
            if response.status_code < 400:
                print(f"    {Fore.BLUE}[HTTP] Active Website: {full_domain} ({response.status_code}){Style.RESET_ALL}")
                with open(output_file, 'a') as f:
                    f.write(f"{full_domain}\n")
        except requests.RequestException:
            pass  # Subdomain resolved but no HTTP response

    except dns.resolver.NXDOMAIN:
        pass  # Subdomain does not exist
    except Exception as e:
        print(f"{Fore.RED}[!] Error resolving {full_domain}: {e}{Style.RESET_ALL}")

# Function to detect wildcard DNS
def is_wildcard(domain):
    try:
        test_sub = f"random-nonexistent.{domain}"
        response = dns.resolver.resolve(test_sub, 'A')
        return True  # If it resolves, it's a wildcard
    except dns.resolver.NXDOMAIN:
        return False  # No wildcard detected
    except Exception as e:
        print(f"{Fore.YELLOW}[!] Wildcard check error: {e}{Style.RESET_ALL}")
        return False

# Main function
def subdomain_enum(domain, wordlist, output_file, threads=10):
    print(f"Starting subdomain enumeration for: {domain}")

    # Check for wildcard DNS
    if is_wildcard(domain):
        print(f"{Fore.YELLOW}[!] Warning: Wildcard DNS detected, results may include false positives!{Style.RESET_ALL}")

    try:
        with open(wordlist, 'r') as file:
            subdomains = [sub.strip() for sub in file.readlines()]
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Wordlist file '{wordlist}' not found!{Style.RESET_ALL}")
        return

    # Ensure output file exists
    if not os.path.exists(output_file):
        open(output_file, 'w').close()

    # Using ThreadPoolExecutor for multi-threading
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for sub in subdomains:
            if stop_event.is_set():
                break
            executor.submit(check_subdomain, domain, sub, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Subdomain Enumerator")
    parser.add_argument("domain", help="Target domain to enumerate")
    parser.add_argument("wordlist", help="Path to the wordlist")
    parser.add_argument("--output", default="output.txt", help="Output file name (default: output.txt)")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads (default: 10)")
    args = parser.parse_args()

    print(f"Press Ctrl+C to stop at any time.")
    subdomain_enum(args.domain, args.wordlist, args.output, threads=args.threads)
    print(f"Results saved to {args.output}")

#example usage for reference --$ python subdomain_enum.py example.com wordlist.txt --output results.txt --threads 20