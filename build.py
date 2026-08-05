import urllib.request
from datetime import datetime
import re

VERSION = "1.0.0"
SOURCES_FILE = "sources.txt"
OUTPUT_FILE = "Blocklist.txt"
STATS_FILE = "Stats.txt"


def download(url):
    print(f"Downloading: {url}")

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "PiHoleBlocklist-Updater/1.0"
            }
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            return response.read().decode("utf-8", errors="ignore")

    except Exception as e:
        print(f"FAILED: {url}")
        print(e)
        return ""


def clean_domain(domain):

    domain = domain.strip().lower()

    # Adblock format
    if domain.startswith("||"):
        domain = domain[2:]

    domain = domain.replace("^", "")
    domain = domain.replace("/", "")

    # Remove ports
    domain = domain.split(":")[0]

    return domain


def extract_domains(text):

    domains = set()

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        if line.startswith("#") or line.startswith("!"):
            continue


        # Remove comments
        line = line.split("#")[0].strip()


        parts = line.split()


        # Hosts format
        if len(parts) >= 2:
            domain = parts[-1]

        else:
            domain = parts[0]


        domain = clean_domain(domain)


        # Validation

        if "*" in domain:
            continue

        if "://" in domain:
            continue

        if re.match(r"^[0-9.]+$", domain):
            continue

        if "." not in domain:
            continue

        if len(domain) < 4:
            continue


        domains.add(domain)


    return domains



def main():

    all_domains = set()
    statistics = {}


    with open(SOURCES_FILE, "r") as file:

        sources = [
            x.strip()
            for x in file.readlines()
            if x.strip()
        ]



    for source in sources:

        data = download(source)

        domains = extract_domains(data)

        statistics[source] = len(domains)

        print(
            f"{len(domains)} domains found"
        )

        all_domains.update(domains)



    domains = sorted(all_domains)



    header = f"""
# PiHoleBlocklist v{VERSION}
# Automatically generated
#
# Sources: {len(sources)}
# Domains: {len(domains)}
# Updated: {datetime.utcnow()} UTC
#
# Do not edit manually.
#

""".lstrip()



    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:

        file.write(header)

        file.write(
            "\n".join(domains)
        )



    with open(STATS_FILE, "w", encoding="utf-8") as file:

        file.write(
f"""PiHoleBlocklist Statistics

Last update:
{datetime.utcnow()} UTC


Sources:
{len(sources)}


Total unique domains:
{len(domains)}


Source breakdown:

"""
        )


        for source, amount in statistics.items():

            file.write(
                f"{source}: {amount}\n"
            )



    print()
    print("==============================")
    print(
        f"TOTAL DOMAINS: {len(domains)}"
    )
    print("==============================")



if __name__ == "__main__":
    main()
