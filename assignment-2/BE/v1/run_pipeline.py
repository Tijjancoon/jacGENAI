#!/usr/bin/env python3
"""
run_pipeline.py
Simple orchestration script (v1) that:
 - clones a repo
 - builds a file map
 - summarizes README
 - parses prioritized files (naive regex)
 - builds a simple CCG
 - writes outputs/<repo_name>/docs.md
Usage:
    python3 run_pipeline.py <git_repo_url>
"""
import sys
import os
from repo_mapper import map_repo, summarize_readme, prioritize
from code_analyzer import build_ccg
from docgenie import generate_markdown
import libs.py_helpers as pyh

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run_pipeline.py <git_repo_url>")
        sys.exit(2)
    url = sys.argv[1]
    print("Validating URL...")
    if not pyh.is_valid_git_url(url):
        print("Invalid git URL:", url)
        sys.exit(1)

    out_base = pyh.ensure_outputs_dir()
    print("Cloning repository...")
    path = pyh.clone_repo(url, out_base)
    if not path:
        print("Clone failed. Ensure git is installed and the repo is accessible.")
        sys.exit(1)

    print("Mapping repo files...")
    file_tree = map_repo(path)

    print("Summarizing README...")
    readme_sum = summarize_readme(path)

    print("Prioritizing targets...")
    targets = prioritize(file_tree, root=path)
    print("Targets:", targets)

    print("Building Code Context Graph...")
    ccg = build_ccg(path, targets)

    repo = {
        "url": url,
        "local_path": path,
        "map": file_tree,
        "readme_summary": readme_sum,
        "ccg": ccg,
        "out_dir": out_base
    }

    print("Generating markdown docs...")
    md_path = generate_markdown(repo, out_base)
    print("Done. Documentation saved to:", md_path)
    print("Exiting.")

if __name__ == "__main__":
    main()
