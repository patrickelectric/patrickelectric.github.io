#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.32.0",
# ]
# ///
"""Search Discogs and maintain the Vinyl shelf catalog.

Set DISCOGS_TOKEN to a personal access token, then run:
  ./catalog.py search "Joni Mitchell Blue"
  ./catalog.py add want 12345
  ./catalog.py move 12345
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile
import webbrowser

import requests


API_URL = "https://api.discogs.com"
CATALOG = Path(__file__).with_name("records.json")
SECTIONS = {"wanted": "wanted", "want": "wanted", "whant": "wanted", "owned": "owned", "have": "owned"}


def section(value: str) -> str:
    try:
        return SECTIONS[value.lower()]
    except KeyError as error:
        raise argparse.ArgumentTypeError("use wanted/want or owned/have") from error


def load_catalog(path: Path) -> dict[str, list[dict]]:
    try:
        catalog = json.loads(path.read_text())
    except FileNotFoundError:
        catalog = {}
    except json.JSONDecodeError as error:
        raise SystemExit(f"{path}: invalid JSON: {error}") from error
    for name in {"wanted", "owned"}:
        entries = catalog.setdefault(name, [])
        if not isinstance(entries, list):
            raise SystemExit(f"{path}: {name} must be an array")
    return catalog


def save_catalog(path: Path, catalog: dict[str, list[dict]]) -> None:
    with tempfile.NamedTemporaryFile("w", dir=path.parent, encoding="utf-8", delete=False) as file:
        json.dump(catalog, file, ensure_ascii=False, indent=2)
        file.write("\n")
        temporary = Path(file.name)
    temporary.replace(path)


def api_get(path: str, **params: str | int) -> dict:
    headers = {"User-Agent": "vinyl-shelf/1.0 +https://patrickelectric.work/vinyl"}
    if token := os.environ.get("DISCOGS_TOKEN"):
        headers["Authorization"] = f"Discogs token={token}"
    try:
        response = requests.get(f"{API_URL}{path}", headers=headers, params=params, timeout=20)
        response.raise_for_status()
    except requests.RequestException as error:
        raise SystemExit(f"Discogs request failed: {error}") from error
    return response.json()


def search(query: str, limit: int) -> None:
    results = api_get("/database/search", q=query, type="release", format="Vinyl", per_page=limit).get("results", [])
    if not results:
        print("No vinyl releases found.")
        return
    print(f"{'ID':>8}  {'YEAR':>4}  RELEASE  FORMAT")
    for result in results:
        formats = ", ".join(result.get("format", []))
        title = result["title"]
        link = f"\033]8;;https://www.discogs.com/release/{result['id']}\033\\{title}\033]8;;\033\\"
        print(f"{result['id']:>8}  {result.get('year', '—'):>4}  {link}  [{formats}]")


def release_name(release: dict) -> str:
    artist = release.get("artists_sort") or ", ".join(item["name"] for item in release.get("artists", []))
    return f"{artist} - {release['title']}" if artist else release["title"]


def release_link(release: dict) -> str:
    return f"\033]8;;https://www.discogs.com/release/{release['id']}\033\\{release_name(release)}\033]8;;\033\\"


def list_catalog(catalog: dict[str, list[dict]], source: str | None) -> None:
    sources = [source] if source else ["wanted", "owned"]
    for index, name in enumerate(sources):
        if index:
            print()
        print(name.upper())
        print(f"{'ID':>8}  {'YEAR':>4}  RELEASE")
        for release in catalog[name]:
            print(f"{release['id']:>8}  {str(release.get('year') or release.get('released', '—'))[:4]:>4}  {release_link(release)}")


def open_release(release_id: int) -> None:
    url = f"https://www.discogs.com/release/{release_id}"
    if not webbrowser.open_new_tab(url):
        raise SystemExit(f"Could not open a browser. URL: {url}")
    print(f"Opened {url}")


def add(catalog: dict[str, list[dict]], destination: str, release_id: int, path: Path) -> None:
    if any(release.get("id") == release_id for releases in catalog.values() for release in releases):
        raise SystemExit(f"Release {release_id} is already in the catalog.")
    release = api_get(f"/releases/{release_id}")
    if not any(item.get("name") == "Vinyl" for item in release.get("formats", [])):
        raise SystemExit(f"Release {release_id} is not a vinyl release.")
    catalog[destination].append(release)
    save_catalog(path, catalog)
    print(f"Added {release['title']} to {destination}.")


def move(catalog: dict[str, list[dict]], release_id: int, source: str, destination: str, path: Path) -> None:
    if source == destination:
        raise SystemExit("Source and destination are the same.")
    for index, release in enumerate(catalog[source]):
        if release.get("id") == release_id:
            catalog[destination].append(catalog[source].pop(index))
            save_catalog(path, catalog)
            print(f"Moved {release['title']} from {source} to {destination}.")
            return
    raise SystemExit(f"Release {release_id} is not in {source}.")


def remove(catalog: dict[str, list[dict]], release_id: int, source: str | None, path: Path) -> None:
    for name in [source] if source else ["wanted", "owned"]:
        for index, release in enumerate(catalog[name]):
            if release.get("id") == release_id:
                catalog[name].pop(index)
                save_catalog(path, catalog)
                print(f"Removed {release['title']} from {name}.")
                return
    location = source or "the catalog"
    raise SystemExit(f"Release {release_id} is not in {location}.")


def parser() -> argparse.ArgumentParser:
    argument_parser = argparse.ArgumentParser(description="Search Discogs and update static/vinyl/records.json.")
    argument_parser.add_argument("--file", type=Path, default=CATALOG, help="catalog JSON file (default: records.json beside this script)")
    commands = argument_parser.add_subparsers(dest="command", required=True)

    search_command = commands.add_parser("search", help="search Discogs for vinyl releases")
    search_command.add_argument("query", nargs="+", help="artist, album, or other Discogs search text")
    search_command.add_argument("--limit", type=int, choices=range(1, 101), default=10)

    open_command = commands.add_parser("open", help="open a Discogs release page in the default browser")
    open_command.add_argument("release_id", type=int)

    list_command = commands.add_parser("list", help="list saved releases")
    list_command.add_argument("--from", dest="source", type=section, metavar="WANT|HAVE")

    add_command = commands.add_parser("add", help="fetch a Discogs release and add it to the catalog")
    add_command.add_argument("destination", type=section, metavar="WANT|HAVE")
    add_command.add_argument("release_id", type=int)

    move_command = commands.add_parser("move", help="move a saved release between sections")
    move_command.add_argument("release_id", type=int)
    move_command.add_argument("--from", dest="source", type=section, default="wanted", metavar="WANT")
    move_command.add_argument("--to", dest="destination", type=section, default="owned", metavar="HAVE")

    remove_command = commands.add_parser("remove", help="remove a saved release")
    remove_command.add_argument("release_id", type=int)
    remove_command.add_argument("--from", dest="source", type=section, metavar="WANT|HAVE")
    return argument_parser


def main() -> None:
    arguments = parser().parse_args()
    if arguments.command == "search":
        search(" ".join(arguments.query), arguments.limit)
        return
    if arguments.command == "open":
        open_release(arguments.release_id)
        return
    catalog = load_catalog(arguments.file)
    if arguments.command == "list":
        list_catalog(catalog, arguments.source)
    elif arguments.command == "add":
        add(catalog, arguments.destination, arguments.release_id, arguments.file)
    elif arguments.command == "move":
        move(catalog, arguments.release_id, arguments.source, arguments.destination, arguments.file)
    else:
        remove(catalog, arguments.release_id, arguments.source, arguments.file)


if __name__ == "__main__":
    main()
