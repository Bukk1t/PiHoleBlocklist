import urllib.request
from datetime import datetime, timezone
from pathlib import Path
import re

VERSION = "1.0.0"

SOURCES_FILE = "sources.txt"
OUTPUT_FILE = "Blocklist.txt"
STATS_FILE = "Stats.txt"


def download(url):
    print(f"\nDownloading: {url}")

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "PiHoleBlocklist-Updater/1.0"
            }
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read().decode(
                "utf-8",
                errors="ignore"
            )

        if not data.strip():
            raise RuntimeError("Downloaded file is empty")

        print(f"Downloaded {len(data):,} bytes")

        return data

    except Exception as e:
        print(f"FAILED: {url}")
        print(f"Reason: {e}")

        raise RuntimeError(
            f"Failed to download source: {url}"
        ) from e


def clean_domain(domain):
    domain = domain.strip().lower()

    domain = domain.split("#", 1)[0].strip()

    if domain.startswith("||"):
        domain = domain[2:]

    if "^" in domain:
        domain = domain.split("^", 1)[0]

    if "$" in domain:
        domain = domain.split("$", 1)[0]

    domain = re.sub(
        r"^[a-z]+://",
        "",
        domain
    )

    domain = domain.split("/", 1)[0]
    domain = domain.split(":", 1)[0]
    domain = domain.strip(".")

    return domain


def is_valid_domain(domain):
    if not domain:
        return False

    if any(char in domain for char in "*?=/"):
        return False

    if ":" in domain:
        return False

    if re.fullmatch(
        r"(?:\d{1,3}\.){3}\d{1,3}",
        domain
    ):
        return False

    if "." not in domain:
        return False

    if len(domain) < 4 or len(domain) > 253:
        return False

    if not re.fullmatch(
        r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?",
        domain
    ):
        return False

    if ".." in domain:
        return False

    for label in domain.split("."):
        if not label:
            return False

        if len(label) > 63:
            return False

        if label.startswith("-") or label.endswith("-"):
            return False

    return True


def extract_domains(text):
    domains = set()

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        if line.startswith("#") or line.startswith("!"):
            continue

        line = line.split("#", 1)[0].strip()

        if not line:
            continue

        parts = line.split()

        if (
            len(parts) >= 2
            and parts[0] in {
                "0.0.0.0",
                "127.0.0.1",
                "::",
                "::1"
            }
        ):
            domain = parts[1]
        else:
            domain = parts[0]

        domain = clean_domain(domain)

        if is_valid_domain(domain):
            domains.add(domain)

    return domains


def load_sources():
    path = Path(SOURCES_FILE)

    if not path.exists():
        raise RuntimeError(
            f"{SOURCES_FILE} does not exist"
        )

    sources = []

    with path.open(
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            sources.append(line)

    if not sources:
        raise RuntimeError("No sources found")

    return sources


def write_blocklist(domains, sources):
    updated = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline="\n"
    ) as file:

        file.write(
            f"# PiHoleBlocklist v{VERSION}\n"
            f"# Automatically generated\n"
            f"# Sources: {len(sources)}\n"
            f"# Domains: {len(domains):,}\n"
            f"# Updated: {updated}\n"
            f"#\n"
            f"# Do not edit manually.\n\n"
        )

        for domain in domains:
            file.write(domain + "\n")


def write_stats(domains, sources, statistics):
    updated = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    with open(
        STATS_FILE,
        "w",
        encoding="utf-8",
        newline="\n"
    ) as file:

        file.write("PiHoleBlocklist Statistics\n")
        file.write("===========================\n\n")

        file.write(f"Version:\n{VERSION}\n\n")
        file.write(f"Last update:\n{updated}\n\n")
        file.write(f"Sources:\n{len(sources)}\n\n")
        file.write(
            f"Total unique domains:\n"
            f"{len(domains):,}\n\n"
        )

        file.write("Source breakdown:\n")

        for source, amount in statistics.items():
            file.write(
                f"{source}: {amount:,}\n"
            )


def main():
    print("==============================")
    print("PiHoleBlocklist Builder")
    print(f"Version {VERSION}")
    print("==============================")

    sources = load_sources()

    print(f"\nLoaded {len(sources)} sources.")

    all_domains = set()
    statistics = {}

    for source in sources:
        data = download(source)

        domains = extract_domains(data)

        if not domains:
            raise RuntimeError(
                "Source returned zero valid domains:\n"
                f"{source}"
            )

        statistics[source] = len(domains)

        print(
            f"Valid domains found: "
            f"{len(domains):,}"
        )

        all_domains.update(domains)

        print(
            f"Current unique total: "
            f"{len(all_domains):,}"
        )

    domains = sorted(all_domains)

    print("\n==============================")
    print(
        f"TOTAL DOMAINS: "
        f"{len(domains):,}"
    )
    print("==============================")

    write_blocklist(
        domains,
        sources
    )

    write_stats(
        domains,
        sources,
        statistics
    )

    print("\n==============================")
    print("BUILD COMPLETE")
    print("==============================")

    print(
        f"Total domains: "
        f"{len(domains):,}"
    )

    print(f"- {OUTPUT_FILE}")
    print(f"- {STATS_FILE}")


if __name__ == "__main__":
    main()
