# gitflattener

Flatten a Git repository into a single plain text or Markdown file — ideal for use as context for large language models (LLMs).

This tool respects `.gitignore`, skips binary files (with optional links), and provides clean, easy-to-ingest output.

## Features

✅ Respects `.gitignore` via `git ls-files`  
✅ Skips binary files with optional source links  
✅ Plain text or Markdown output  
✅ Minimal dependencies, Python 3.12+  
✅ CLI-ready (`gitflattener` command)

## Installation

```bash
git clone https:// .... / gitflattener.git
cd gitflattener
pip install .
```

### Options

| Argument              | Description                                          |
|------------------------|------------------------------------------------------|
| `repo_path`            | Path to local Git repository                         |
| `output_path`          | Output file (plain text or Markdown)                 |
| `--markdown`           | Format output using Markdown headers                 |
| `--base-url <url>`     | Link binary files to remote repo (e.g., GitLab URL)  |
