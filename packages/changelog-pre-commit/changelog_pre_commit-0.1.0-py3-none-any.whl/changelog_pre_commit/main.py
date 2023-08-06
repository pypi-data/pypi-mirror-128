from pathlib import Path

from git import Repo


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
repo = Repo(BASE_DIR)

modified_files_full_path = [
    file.a_path.lower() for file in repo.index.diff(repo.head.commit)
]
modified_files = [Path(x).stem for x in modified_files_full_path]

if not any(file == "changelog" for file in modified_files):
    raise Exception("You didn't update the changelog file :(")
