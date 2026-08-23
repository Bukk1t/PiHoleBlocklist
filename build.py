import urllib.request
from datetime import datetime, timezone
from pathlib import Path
import re
import math

VERSION = "1.1.0"

SOURCES_FILE = "sources.txt"
STATS_FILE = "Stats.txt"

# Keep comfortably below GitHub's 100 MB hard limit.
MAX_PART_SIZE = 90 * 1024 * 1024

OUTPUT_PREFIX = "Blocklist"


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
            data = response.read().decode(
                "utf-8",
                errors="ignore"
            )

        if not data.strip():
            raise RuntimeError(
                "Downloaded file is empty"
            )

        print(
            f"Downloaded {len(data):,} bytes"
        )

        return data

    except Exception as e:
        print(f"FAILED: {url}")
        print(f"Reason: {e}")

        raise RuntimeError(
            f"Failed to download source: {url}"
        ) from e


def clean_domain(domain):
    domain = domain.strip().lower()

    # Remove inline comments
    domain = domain.split("#", 1)[0].strip()

    # AdBlock / uBlock format
    if domain.startswith("||"):
        domain = domain[2:]

    # Remove AdBlock modifiers
    if "^" in domain:
        domain = domain.split("^", 1)[0]

    if "$" in domain:
        domain = domain.split("$", 1)[0]

    # Remove URL scheme
    domain = re.sub(
        r"^[a-z]+://",
        "",
        domain
    )

    # Remove path
    domain = domain.split("/", 1)[0]

    # Remove port
    domain = domain.split(":", 1)[0]

    # Remove trailing dot
    domain = domain.strip(".")

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

    # Reject IPv4 addresses
    if re.fullmatch(
        r"(?:\d{1,3}\.){3}\d{1,3}",
        domain
    ):
        return False

    # Must contain a dot
    if "." not in domain:
        return False

    # Valid length
    if len(domain) < 4 or len(domain) > 253:
        return False

    # Valid domain characters
    if not re.fullmatch(
        r"[a-z0-9](?:[a-z0-9.-]*[a-z0-9])?",
        domain
    ):
        return False

    # No consecutive dots
    if ".." in domain:
        return False

    # Validate labels
    for label in domain.split("."):
        if not label:
            return False

        if len(label) > 63:
            return False

        if (
            label.startswith("-")
            or label.endswith("-")
        ):
            return False

    return True


def extract_domains(text):
    domains = set()

    for raw_line in text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        # Comments
        if (
            line.startswith("#")
            or line.startswith("!")
        ):
            continue

        # Remove inline comments
        line = line.split("#", 1)[0].strip()

        if not line:
            continue

        parts = line.split()

        # Hosts file format
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

            if not line:
                continue

            if line.startswith("#"):
                continue

            sources.append(line)

    if not sources:
        raise RuntimeError(
            "No sources found"
        )

    return sources


def header(domains_count, sources_count):
    updated = datetime.now(
        timezone.utc
    ).strftime(
        "%Y-%m-%d %H:%M:%S UTC"
    )

    return (
        f"# PiHoleBlocklist v{VERSION}\n"
        f"# Automatically generated\n"
        f"#\n"
        f"# Sources: {sources_count}\n"
        f"# Domains: {domains_count:,}\n"
        f"# Updated: {updated}\n"
        f"#\n"
        f"# Do not edit manually.\n"
        f"#\n\n"
    )


def delete_old_parts():
    """
    Remove old generated blocklist parts so that
    deleted/obsolete parts don't remain in Git.
    """

    for path in Path(".").glob(
        f"{OUTPUT_PREFIX}-*.txt"
    ):
        print(
            f"Removing old part: {path}"
        )

        path.unlink()


def split_blocklist(domains, sources):
    """
    Split the complete blocklist into files that
    stay below MAX_PART_SIZE.
    """

    delete_old_parts()

    total_domains = len(domains)

    current_part = []
    current_size = 0
    parts = []

    # Generate the common header.
    base_header = header(
        total_domains,
        len(sources)
    )

    header_size = len(
        base_header.encode("utf-8")
    )

    for domain in domains:

        line = domain + "\n"

        line_size = len(
            line.encode("utf-8")
        )

        # If adding this domain would exceed
        # the limit, finish the current part.
        if (
            current_part
            and current_size
            + line_size
            + header_size
            > MAX_PART_SIZE
        ):

            parts.append(current_part)

            current_part = []
            current_size = 0

        current_part.append(domain)
        current_size += line_size

    # Add final part
    if current_part:
        parts.append(current_part)

    total_parts = len(parts)

    print("\n==============================")
    print(
        f"Splitting into {total_parts} parts"
    )
    print(
        f"Maximum part size: "
        f"{MAX_PART_SIZE / 1024 / 1024:.0f} MB"
    )
    print("==============================")

    generated_files = []

    for index, part_domains in enumerate(
        parts,
        start=1
    ):

        filename = (
            f"{OUTPUT_PREFIX}-"
            f"{index:02d}.txt"
        )

        part_header = header(
            total_domains,
            len(sources)
        )

        content = (
            part_header
            + "\n".join(part_domains)
            + "\n"
        )

        path = Path(filename)

        path.write_text(
            content,
            encoding="utf-8",
            newline="\n"
        )

        size = path.stat().st_size

        print(
            f"{filename}: "
            f"{len(part_domains):,} domains "
            f"({size / 1024 / 1024:.2f} MB)"
        )

        if size > MAX_PART_SIZE:
            raise RuntimeError(
                f"{filename} exceeds the "
                f"maximum allowed size."
            )

        generated_files.append(
            (filename, len(part_domains), size)
        )

    return generated_files


def write_stats(
    domains,
    sources,
    statistics,
    generated_files
):
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

        file.write(
            "PiHoleBlocklist Statistics\n"
        )

        file.write(
            "===========================\n\n"
        )

        file.write(
            f"Version:\n{VERSION}\n\n"
        )

        file.write(
            f"Last update:\n{updated}\n\n"
        )

        file.write(
            f"Sources:\n"
            f"{len(sources)}\n\n"
        )

        file.write(
            f"Total unique domains:\n"
            f"{len(domains):,}\n\n"
        )

        file.write(
            f"Blocklist parts:\n"
            f"{len(generated_files)}\n\n"
        )

        file.write(
            "Generated files:\n"
        )

        for (
            filename,
            amount,
            size
        ) in generated_files:

            file.write(
                f"{filename}: "
                f"{amount:,} domains, "
                f"{size / 1024 / 1024:.2f} MB\n"
            )

        file.write(
            "\nSource breakdown:\n"
        )

        for source, amount in statistics.items():

            file.write(
                f"{source}: "
                f"{amount:,}\n"
            )


def main():

    print("==============================")
    print("PiHoleBlocklist Builder")
    print(f"Version {VERSION}")
    print("==============================")

    sources = load_sources()

    print(
        f"\nLoaded {len(sources)} sources."
    )

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

    generated_files = split_blocklist(
        domains,
        sources
    )

    write_stats(
        domains,
        sources,
        statistics,
        generated_files
    )

    print("\n==============================")
    print("BUILD COMPLETE")
    print("==============================")

    print(
        f"Total domains: "
        f"{len(domains):,}"
    )

    print(
        f"Parts generated: "
        f"{len(generated_files)}"
    )

    for filename, _, _ in generated_files:
        print(f"- {filename}")

    print(f"- {STATS_FILE}")


if __name__ == "__main__":
    main()
