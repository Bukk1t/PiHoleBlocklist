import urllib.request
from datetime import datetime, timezone
from pathlib import Path
import re

VERSION = "1.1.0"

SOURCES_FILE = "sources.txt"
OUTPUT_FILE = "Blocklist.txt"
STATS_FILE = "Stats.txt"

# Drop protection
MAX_DROP_PERCENT = 15.0


def download(url):
    print(f"\nDownloading: {url}")

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "PiHoleBlocklist-Updater/1.1"
            }
        )

        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read().decode("utf-8", errors="ignore")

        if not data.strip():
            raise RuntimeError("Downloaded file is empty")

        print(f"Downloaded {len(data):,} bytes")
        return data

    except Exception as e:
        print(f"FAILED: {url}")
        print(f"Reason: {e}")
        raise RuntimeError(f"Failed to download source: {url}") from e


def clean_domain(domain):
    domain = domain.strip().lower()

    # Remove inline comments
    domain = domain.split("#", 1)[0].strip()

    # AdBlock / uBlock format
    if domain.startswith("||"):
        domain = domain[2:]

    # Hosts file format
    if domain.startswith("0.0.0.0 "):
        domain = domain.split(None, 1)[1]

    if domain.startswith("127.0.0.1 "):
        domain = domain.split(None, 1)[1]

    # Remove leading/trailing dots
    domain = domain.strip(".")

    # Remove AdBlock modifiers
    if "^" in domain:
        domain = domain.split("^", 1)[0]

    # Remove AdGuard/uBlock options
    if "$" in domain:
        domain = domain.split("$", 1)[0]

    # Remove URL scheme
    domain = re.sub(r"^[a-z]+://", "", domain)

    # Remove path
    domain = domain.split("/", 1)[0]

    # Remove port
    domain = domain.split(":", 1)[0]

    # Remove trailing dot
    domain = domain.rstrip(".")

    return domain


def is_valid_domain(domain):
    if not domain:
        return False

    if "*" in domain:
        return False

    if "?" in domain:
        return False

    if "=" in domain:
        return False

    if "/" in domain:
        return False

    if ":" in domain:
        return False

    # Reject IP addresses
    if re.fullmatch(
        r"(?:\d{1,3}\.){3}\d{1,3}",
        domain
    ):
        return False

    # Must contain a dot
    if "." not in domain:
        return False

    # Reasonable domain length
    if len(domain) < 4 or len(domain) > 253:
        return False

    # Valid domain characters
    if not re.fullmatch(
        r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?",
        domain
    ):
        return False

    # Reject consecutive dots
    if ".." in domain:
        return False

    # Reject invalid labels
    labels = domain.split(".")

    for label in labels:
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

        # Comments
        if line.startswith("#"):
            continue

        if line.startswith("!"):
            continue

        if line.startswith("[Adblock"):
            continue

        if line.startswith("[AdGuard"):
            continue

        # Remove inline comments
        line = line.split("#", 1)[0].strip()

        if not line:
            continue

        # ---------------------------------------------------------
        # Hosts format:
        #
        # 0.0.0.0 example.com
        # 127.0.0.1 example.com
        # ---------------------------------------------------------

        parts = line.split()

        if len(parts) >= 2:
            first = parts[0]

            if first in {
                "0.0.0.0",
                "127.0.0.1",
                "::",
                "::1"
            }:
                domain = parts[1]
            else:
                # Don't blindly take the last field from arbitrary
                # filter syntax.
                domain = parts[0]

        else:
            domain = parts[0]

        domain = clean_domain(domain)

        if is_valid_domain(domain):
            domains.add(domain)

    return domains


def load_sources():
    path = Path(SOURCES_FILE)

    if not path.exists():
        raise RuntimeError(f"{SOURCES_FILE} does not exist")

    sources = []

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            if line.startswith("#"):
                continue

            sources.append(line)

    if not sources:
        raise RuntimeError("No sources found")

    return sources


def get_previous_total():
    path = Path(STATS_FILE)

    if not path.exists():
        return None

    try:
        text = path.read_text(encoding="utf-8")

        match = re.search(
            r"Total unique domains:\s*([\d,]+)",
            text
        )

        if match:
            return int(match.group(1).replace(",", ""))

    except Exception:
        pass

    return None


def check_for_suspicious_drop(new_total, previous_total):
    if previous_total is None:
        print("\nNo previous statistics found.")
        print("Skipping drop protection for first build.")
        return

    if previous_total <= 0:
        return

    drop_percent = (
        (previous_total - new_total)
        / previous_total
        * 100
    )

    print("\nPrevious domains:", f"{previous_total:,}")
    print("New domains:     ", f"{new_total:,}")
    print("Change:           ", f"{-drop_percent:.2f}%")

    if drop_percent > MAX_DROP_PERCENT:
        raise RuntimeError(
            "\nBLOCKLIST UPDATE STOPPED!\n"
            f"The blocklist dropped by {drop_percent:.2f}%.\n"
            f"Previous: {previous_total:,}\n"
            f"New:      {new_total:,}\n"
            f"Maximum allowed drop: {MAX_DROP_PERCENT}%\n"
            "\n"
            "This may indicate that an upstream source "
            "is missing or broken."
        )


def write_blocklist(domains, sources):
    updated = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    header = (
        f"# PiHoleBlocklist v{VERSION}\n"
        f"# Automatically generated\n"
        f"#\n"
        f"# Sources: {len(sources)}\n"
        f"# Domains: {len(domains):,}\n"
        f"# Updated: {updated}\n"
        f"#\n"
        f"# Do not edit manually.\n"
        f"#\n"
        f"\n"
    )

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8",
        newline="\n"
    ) as file:
        file.write(header)
        file.write("\n".join(domains))
        file.write("\n")


def write_stats(domains, sources, statistics):
    updated = datetime.now(timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    with open(
        STATS_FILE,
        "w",
        encoding="utf-8",
        newline="\n"
    ) as file:

        file.write(
            "PiHoleBlocklist Statistics\n"
            "==========================\n\n"
        )

        file.write(
            f"Version:\n{VERSION}\n\n"
        )

        file.write(
            f"Last update:\n{updated}\n\n"
        )

        file.write(
            f"Sources:\n{len(sources)}\n\n"
        )

        file.write(
            f"Total unique domains:\n{len(domains):,}\n\n"
        )

        file.write(
            "Source breakdown:\n"
            "------------------\n\n"
        )

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
                f"Source returned zero valid domains:\n{source}"
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
        f"TOTAL DOMAINS: {len(domains):,}"
    )
    print("==============================")

    previous_total = get_previous_total()

    check_for_suspicious_drop(
        len(domains),
        previous_total
    )

    write_blocklist(
        domains,
        sources
    )

    write_stats(
        domains,
        sources,
        statistics
    )

    print("\nFiles generated successfully:")
    print(f"- {OUTPUT_FILE}")
    print(f"- {STATS_FILE}")


if __name__ == "__main__":
    main()
