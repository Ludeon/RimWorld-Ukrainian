#!/usr/bin/env python3
import argparse
import os
import os.path
import tempfile
import urllib.request
import zipfile


def main(args):
    parser = argparse.ArgumentParser(
        description="Replace local files with latest version from CrowdIn."
    )
    parser.add_argument(
        "-p",
        "--project-identifier",
        help="Crowdin project identifier",
        default=os.environ.get("PROJECT_IDENTIFIER", 'rimworld-ukr'),
    )
    parser.add_argument(
        "-k",
        "--project-key",
        help="Crowdin API project key",
        default=os.environ.get("PROJECT_KEY"),
    )
    parsed_args = parser.parse_args(args)
    if not parsed_args.project_identifier:
        raise
    if not parsed_args.project_key:
        raise

    project = CrowdinProject(parsed_args.project_identifier, parsed_args.project_key)
    archive = project.download_archive()
    translations_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    project.extract_archive(archive, translations_root)


class CrowdinProject:
    BASE_URL = "https://api.crowdin.com/api/project"

    def __init__(self, project_identifier, project_key):
        self.project_identifier = project_identifier
        self.project_key = project_key

    def download_archive(self):
        url = f"{self.BASE_URL}/{self.project_identifier}/download/uk.zip?key={self.project_key}"
        print(url)

        (archive_path, _) = urllib.request.urlretrieve(url)
        archive = zipfile.ZipFile(archive_path)
        return archive

    def extract_archive(self, archive: zipfile.ZipFile, target_dir):
        prefix = "master/"
        for info in archive.infolist():
            print(info)
            assert info.filename.startswith(prefix)
            path = os.path.join(target_dir, info.filename[len(prefix) :])
            if _is_dir(info):
                os.makedirs(path, exist_ok=True)
            else:
                content = archive.read(info)
                with open(path, "wb") as f:
                    f.write(content)


def _is_dir(zipinfo):
    """Determine if zipinfo object corresponds to a directory.

    It was observed that directories paths have a trailing slash.
    """
    return zipinfo.filename.endswith("/")


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
