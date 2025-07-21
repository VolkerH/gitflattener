from pathlib import Path
import subprocess
import mimetypes
from collections.abc import Iterable

def get_git_tracked_files(repo_path: Path) -> list[str]:
    """
    Get the list of files tracked by git, respecting .gitignore.
    """
    try:
        result = subprocess.run(
            ["git", "-C", str(repo_path), "ls-files", "--exclude-standard"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        files = result.stdout.strip().splitlines()
        return files
    except subprocess.CalledProcessError as e:
        print(f"Error running git ls-files: {e.stderr}")
        return []


def is_binary_file(filepath: Path, blocksize: int = 512) -> bool:
    """
    Detect if a file is binary.
    """
    try:
        chunk = filepath.read_bytes()[:blocksize]
        if b'\0' in chunk:
            return True
        match mimetypes.guess_type(filepath.name):
            case (mime, _) if mime and not mime.startswith("text"):
                return True
        return False
    except Exception:
        return True


def flatten_repo(
    repo_path: Path,
    output_path: Path,
    base_url: str | None = None,
    markdown: bool = False
) -> None:
    """
    Flatten a Git repository into a single text or Markdown file.
    """
    files: Iterable[str] = get_git_tracked_files(repo_path)
    if not files:
        print("No tracked files found.")
        return

    with output_path.open("w", encoding="utf-8") as out:
        for relpath in files:
            filepath = repo_path / relpath
            if not filepath.is_file():
                continue

            header = (
                f"\n## `{relpath}`\n\n"
                if markdown else
                f"\n{'='*80}\nFILE: {relpath}\n{'='*80}\n\n"
            )
            out.write(header)

            if is_binary_file(filepath):
                link = (
                    f"[Binary file omitted: {base_url}/-/blob/main/{relpath}]\n"
                    if base_url else
                    f"[Binary file omitted: {relpath}]\n"
                )
                out.write(link)
                continue

            try:
                content = filepath.read_text(encoding="utf-8")
                out.write(content + "\n")
            except Exception as e:
                out.write(f"[Could not read file: {relpath}. Error: {e}]\n")

    print(f"Flattened repository written to {output_path}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Flatten a Git repo into a single text or Markdown file."
    )
    parser.add_argument("repo_path", type=Path, help="Path to local Git repository.")
    parser.add_argument("output_path", type=Path, help="Output text or Markdown file path.")
    parser.add_argument("--base-url", type=str, help="Base URL for binary file links (optional).")
    parser.add_argument("--markdown", action="store_true", help="Output as Markdown with headers.")

    args = parser.parse_args()

    flatten_repo(
        repo_path=args.repo_path,
        output_path=args.output_path,
        base_url=args.base_url,
        markdown=args.markdown,
    )


if __name__ == "__main__":
    main()
