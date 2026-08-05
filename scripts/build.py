import urllib.request
from datetime import datetime

SOURCES_FILE = "sources.txt"
OUTPUT_FILE = "Blocklist.txt"


def download(url):
    print(f"Downloading: {url}")
    try:
        with urllib.request.urlopen(url, timeout=30) as response:
            return response.read().decode("utf-8", errors="ignore")
    except Exception as e:
        print(f"Failed: {url} -> {e}")
        return ""


def extract_domains(text):
    domains = set()

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("#") or line.startswith("!"):
            continue

        # hosts format:
        # 0.0.0.0 example.com
        parts = line.split()

        if len(parts) >= 2:
            domain = parts[-1]
        else:
            domain = parts[0]

        # remove comments
        domain = domain.split("#")[0].strip()

        # basic filtering
        if (
            "." in domain
            and " " not in domain
            and "/" not in domain
            and domain not in ["localhost", "localhost.localdomain"]
        ):
            domains.add(domain.lower())

    return domains


def main():
    all_domains = set()

    with open(SOURCES_FILE, "r") as f:
        sources = [
            x.strip()
            for x in f.readlines()
            if x.strip()
        ]

    for source in sources:
        data = download(source)
        all_domains.update(extract_domains(data))

    domains = sorted(all_domains)

    header = f"""# Ultimate Pi-hole Blocklist
# Automatically generated
# Last updated: {datetime.utcnow()} UTC
# Sources: {len(sources)}
# Domains: {len(domains)}
#
# Do not edit manually.
#

"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(domains))

    print(f"Finished! {len(domains)} domains written.")


if __name__ == "__main__":
    main()