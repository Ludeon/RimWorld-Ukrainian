#!/usr/bin/env python3
import argparse
import json
import os
import pathlib
import urllib.request
import zipfile


def main(args):
    parser = argparse.ArgumentParser(
        description="Replace local files with latest version from CrowdIn."
    )
    parser.add_argument(
        "--project-identifier",
        help="Crowdin project identifier",
        default=os.environ.get("PROJECT_IDENTIFIER", "295257"),
    )
    parser.add_argument(
        "--access-token",
        help="Crowdin API v2 access token",
        default=os.environ.get("CROWDIN_ACCESS_TOKEN"),
    )
    parsed_args = parser.parse_args(args)
    if not parsed_args.project_identifier:
        raise ValueError("Project indentifier is missing")
    if not parsed_args.access_token:
        raise ValueError("Access toke is missing")

    project = CrowdinProject(parsed_args.project_identifier, parsed_args.access_token)
    archive = project.download_archive()
    repository_root = pathlib.Path(__file__).parent.parent.parent
    project.extract_archive(archive, repository_root)


class CrowdinProject:
    BASE_URL = "https://api.crowdin.com/api/v2/projects"

    def __init__(self, project_identifier, access_token):
        self.project_identifier = project_identifier
        self.access_token = access_token

        self.opener = urllib.request.build_opener()
        self.opener.addheaders = [("Authorization", f"Bearer {self.access_token}")]

    def download_archive(self):
        build_id = self._get_latest_build_id()
        translation_url = self._get_translation_url(build_id)
        return self._download_archive(translation_url)

    def _get_latest_build_id(self):
        url = f"{self.BASE_URL}/{self.project_identifier}/translations/builds"
        with self.opener.open(url) as response:
            payload = json.load(response)

        build = payload["data"][0]  # checking only the latest build
        if build["data"]["status"] != "finished":
            raise ValueError("Latest build is not finished. Please try again later.")

        return build["data"]["id"]

    def _get_translation_url(self, build_id):
        url = f"{self.BASE_URL}/{self.project_identifier}/translations/builds/{build_id}/download"
        with self.opener.open(url) as response:
            payload = json.load(response)

        return payload["data"]["url"]

    def _download_archive(self, url):
        print(url)
        (archive_path, _) = urllib.request.urlretrieve(url)
        archive = zipfile.ZipFile(archive_path)
        return archive

    def extract_archive(self, archive: zipfile.ZipFile, target_dir: pathlib.Path):
        prefix = "uk/[RimWorld-Ukrainian-Crowdin.RimWorld-English] master/"
        for info in archive.infolist():
            print(info)

            file_name = info.filename[len(prefix) :]
            if file_name.startswith("old/"):
                continue  # skip the "old" folder

            path = target_dir / info.filename[len(prefix) :]
            if _is_dir(info):
                continue  # skip directories

            path.parent.mkdir(exist_ok=True)
            content = archive.read(info)
            with path.open("wb") as f:
                f.write(content)


def _is_dir(zipinfo):
    """Determine if zipinfo object corresponds to a directory.

    It was observed that directories paths have a trailing slash.
    """
    return zipinfo.filename.endswith("/")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
